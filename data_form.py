#!/usr/bin/env python
#coding:utf-8
import xlrd
import numpy as np
from matplotlib.pyplot import *
from delorean import *


class Data():

	def plot(self):
		plot(self.time, self.percent, label=self.filename)

	def second2hour(self):
		for i in range(len(self.time)):
			self.time[i] = self.time[i]/3600.

	@classmethod
	def show(cls,savename="capacity_time",icon='lower right'):
		xlim(0,6)
		title("discharging")
		xlabel("time /h")
		ylabel("capacity /%")
		grid(True)
		legend(loc=icon)
		savefig(savename+'.jpg')
		show()


class Excel_data(Data):

	def __init__(self,filename,sheet=u'Sheet1',percent_col=4,time_col=5):
		self.filename = filename
		self.data = xlrd.open_workbook(filename)
		self.PC_table = self.data.sheet_by_name(sheet)
		self.time = self.PC_table.col_values(time_col)
		self.percent = self.PC_table.col_values(percent_col)
		self.second2hour()

class Log_data(Data):

	def __init__(self,filename):
		self.filename = filename
		self.devie_log = open(self.filename, 'r')
		self.time = []
		self.percent = []
		for line in self.devie_log.readlines():
			time = ' '.join(line.split()[0:2])
			self.time.append(int(parse(time).epoch()))
			percent = line.split()[2].split('%')
			self.percent.append(int(percent[0]))
		m = len(self.time)
		device_time_base = self.time[0]
		for x in range(m):
  			self.time[x] = self.time[x] - device_time_base
  		self.second2hour()

def receive(filenames):
	for f in filenames:
		namesplit = f.split('.')
		if namesplit[1] == 'txt':
			Log_data(f).plot()
		elif namesplit[1] == 'xls':
			Excel_data(f).plot()

if __name__ == '__main__':
	files = ["430_discharge_Book1.xls", "430_discharge_BatteryLog.txt"]
	receive(files)
	Data.show(savename='430_discharge', icon='upper right')
