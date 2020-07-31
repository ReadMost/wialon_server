# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://94.247.135.91:8086/egistic_2.0')
Session = sessionmaker(bind=engine)

Base = declarative_base()