# coding=utf-8

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

engine = create_engine('postgresql://docker:docker@94.247.135.91:8086/egistic_2.0', connect_args={"options": "-c timezone=utc+6"})
# Session = sessionmaker(bind=engine)

Base = declarative_base()

# Base.prepare(engine, reflect=True)

session = Session(engine)

