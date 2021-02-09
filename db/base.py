# coding=utf-8

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .thread_save import init_engine, init_session_factory

engine = init_engine(uri='postgresql://docker:PNdvVpM3VQoMOVOeu8YCbGc69eo2X3iC@94.247.135.91:8050/egistic_2.0')
# Session = sessionmaker(bind=engine)

Base = declarative_base()

# Base.prepare(engine, reflect=True)

# session = Session(engine)
# init_session_factory()
