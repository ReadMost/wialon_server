# coding=utf-8
import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey

from db.base import Base
from geoalchemy2 import Geometry
import pytz

from db.thread_save import ManagedSession, init_session_factory

timezone = pytz.timezone("Asia/Almaty")

class BlackBoxPacket(Base):
	__tablename__ = 'telematics_blackboxpacket'
	id = Column(Integer, primary_key=True, autoincrement=True)
	was_send = Column(Integer, nullable=True)
	was_proceeded = Column(Integer, nullable=True)

	def __init__(self, was_send, was_proceeded):
		self.was_send = was_send
		self.was_proceeded = was_proceeded

	def save(self):
		init_session_factory()
		with ManagedSession() as session:

			session.add(self)
			return self

class ShortPacket(Base):
	__tablename__ = 'telematics_shortpacket'

	id = Column(Integer, primary_key=True, autoincrement=True)
	date_time = Column(DateTime(timezone=True), nullable=True)
	point = Column(Geometry('POINT'), nullable=True)
	speed = Column(Integer, nullable=True)
	course = Column(Integer, nullable=True)
	alt = Column(Integer, nullable=True)
	sats = Column(Integer, nullable=True)
	created_at = Column(DateTime(timezone=True))
	imei = Column(String, nullable=True)
	black_box = Column('black_box_id', Integer, ForeignKey('telematics_blackboxpacket.id'))

	def __init__(self, date_time, point, speed, course, alt, sats, black_box, imei):
		self.date_time = date_time
		self.point = point
		self.speed = speed
		self.course = course
		self.alt = alt
		self.sats = sats
		self.black_box = black_box
		self.imei = imei
		self.created_at = datetime.datetime.now(timezone) + datetime.timedelta(hours=6)



class ExtendedPacket(Base):
	__tablename__ = 'telematics_extendedpacket'

	id = Column(Integer, primary_key=True, autoincrement=True)
	hdop = Column(Float, nullable=True)
	inputs = Column(Integer, nullable=True)
	outputs = Column(Integer, nullable=True)
	adc = Column(String, nullable=True)
	ibutton = Column(String, nullable=True)
	short_packet = Column('short_packet_id', Integer, ForeignKey('telematics_shortpacket.id'))

	def __init__(self, hdop, inputs, outputs, adc, ibutton, short_packet):
		self.hdop = hdop
		self.inputs = inputs
		self.outputs = outputs
		self.adc = adc
		self.ibutton = ibutton
		self.short_packet = short_packet

class Params(Base):
	__tablename__ = 'telematics_params'

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, nullable=True)
	type = Column(Integer, nullable=True)
	value = Column(String, nullable=True)
	extended = Column('extended_id', Integer, ForeignKey('telematics_extendedpacket.id'))

	def __init__(self, name, type, value, extended):
		self.name = name
		self.type = type
		self.value = value
		self.extended = extended


