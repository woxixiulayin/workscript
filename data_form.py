#!/usr/bin/env python
# coding:utf-8
import xlrd
import numpy as np
from matplotlib.pyplot import *
from delorean import *
import logging
logging.basicConfig(level=logging.WARNING)
import os

savename = 'charge'
icon = 'lower right'


class Data():

    def plot(self):
        plot(self.time, self.percent, label=self.filename)

    def second2hour(self):
        for i in range(len(self.time)):
            self.time[i] = self.time[i] / 3600.

    @classmethod
    def receive(cls, filenames):
        for f in filenames:
            namesplit = f.split('.')
            if len(namesplit) == 1:
                continue
            if namesplit[1] == 'txt':
                Log_data(f).plot()
            elif namesplit[1] == 'xls':
                Excel_data(f).plot()
            elif namesplit[1] == 'xlsx':
                logging.warning(
                    'please change file %s to *** .xls *** if you want to use it' % (f))

    @classmethod
    def show(cls):
        global savename, icon
        # xlim(0, xscale)
        title("discharging")
        xlabel("time /h")
        ylabel("capacity /%")
        grid(True)
        legend(loc=icon)
        savefig(savename + '.jpg')
        show()


class Excel_data(Data):

    def __init__(self, filename, sheet=u'Sheet1', time_col=0, current_col=2):
        global savename, icon
        self.filename = filename
        savename = filename.split('.')[0] + '_charge'
        self.file = xlrd.open_workbook(filename)
        self.PC_table = self.file.sheet_by_name(sheet)
        self.time = self.time2second(time_col)
        self.len = len(self.time)
        self.charge = True
        if self.PC_table.col_values(current_col)[10] < 0:
            self.charge = False
            icon = 'upper right'
            savename = filename.split('.')[0] + '_discharge'
        logging.info('the test is %s' %
                     ('charge' if self.charge else 'discharge'))
        self.percent = self.current2percent(current_col)
        self.second2hour()

    def time2second(self, time_col):
        time_second = []
        time_origin = []
        time_float = self.PC_table.col_values(time_col)
        days_index = []
        days_index.append(0)
        for i, v in enumerate(time_float):
            time_origin.append(int(v * 3600 * 24))
            if i > 0 and (time_origin[i] < time_origin[i - 1]):
                days_index.append(i)
        days_index.append(len(time_origin))
        logging.info("days_index is")
        logging.info(days_index)
        for i in range(len(days_index) - 1):
            extra_time = i * 3600 * 24
            for n in range(days_index[i], days_index[i + 1]):
                time_second.append(time_origin[n] + extra_time)
        return time_second

    def current2percent(self, current_col):
        percent = []
        currents = [abs(v) for v in self.PC_table.col_values(current_col)]
        capacity = 0
        capacity_rows = []
        capacity_rows.append(capacity)
        for i in range(1, self.len):
            capacity = round(
                currents[i] * (self.time[i] - self.time[i - 1]) / 3600. + capacity, 2)
            capacity_rows.append(capacity)
        ch_flag = 0 if self.charge else 1
        for i, v in enumerate(capacity_rows):
            logging.info(
                round(abs((v - ch_flag * capacity)) / capacity * 100, 1))
            percent.append(
                round(abs((v - ch_flag * capacity)) / capacity * 100, 1))
        logging.info("capacity is %d" % capacity)
        return percent


class Log_data(Data):

    def __init__(self, filename):
        self.filename = filename
        self.devie_log = open(self.filename, 'r')
        self.time = []
        self.percent = []
        for line in self.devie_log.readlines():
            if len(line.split()) > 1:
                time = ' '.join(line.split()[0:2])
                self.time.append(int(parse(time).epoch()))
                percent = line.split()[2].split('%')
                self.percent.append(int(percent[0]))
        m = len(self.time)
        device_time_base = self.time[0]
        for x in range(m):
            self.time[x] = self.time[x] - device_time_base
        self.second2hour()


def get_files_in_current():
    cur = os.getcwd()
    logging.info(cur)
    files = os.listdir(cur)
    logging.info(files)
    return files


def main():
    files = get_files_in_current()
    Data.receive(files)
    Data.show()

if __name__ == '__main__':
    main()
