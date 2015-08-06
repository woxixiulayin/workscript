#!/usr/bin/env python
from sqlalchemy import Column, String, create_engine,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(String(20), primary_key=True)
	name = Column(String(20))
	books = relationship('Book')

class Book(Base):
	__tablename__ = 'book'
	id = Column(String(20), primary_key=True)
	name = Column(String(20))
	user_id = Column(String(20),ForeignKey('user.id'))


currdir = os.path.join(os.path.dirname(__file__), 'data.sql')
db_url = 'sqlite:///%s' % currdir

engine = create_engine(db_url)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

DBsession = sessionmaker(bind=engine)



