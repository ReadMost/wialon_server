import pytz

from db.db_reflect import ShortRequestSession
from exceptions import *
import datetime
timezone = pytz.timezone("Asia/Almaty")

class ShortRequest(object):
	def __init__(self, socket, imei, black_box):
		self.socket = socket
		self.imei = imei
		self.black_box = black_box
		self._date_time = None
		self._lat = None
		self._lon = None
		self._speed = None
		self._course = None
		self._alt = None
		self._sats = None

	def __repr__(self):
		result = ''
		if self._date_time:
			result += "_date_time:" + str(self._date_time) + ";"
		if self._lat:
			result += "_lat:" + str(self._lat) + ";"
		if self._lon:
			result += "_lon:" + str(self._lon) + ";"
		if self._speed:
			result += "_speed:" + str(self._speed) + ";"
		if self._course:
			result += "_course:" + str(self._course) + ";"
		if self._alt:
			result += "_alt:" + str(self._alt) + ";"
		if self._sats:
			result += "_sats:" + str(self._sats) + ";"
		return result

	def get_latitude(self, coord, direction):
		degree = int(coord[:2])
		minute = float(coord[2:]) / 60
		if direction == "N":
			self._lat = degree + minute
		else:
			self._lat = -1 * (degree + minute)

	def get_longitude(self, coord, direction):
		degree = int(coord[:3])
		minute = float(coord[3:]) / 60
		if direction == "E":
			self._lon = degree + minute
		else:
			self._lon = -1 * (degree + minute)

	'''date and time'''

	@property
	def date_time(self):
		return self._date_time

	@date_time.setter
	def date_time(self, arg):
		try:
			date, time = arg
			date_time = None
			if not date == "NA":
				if not time == "NA":
					date_time = datetime.datetime.strptime(date + " " + time, '%d%m%y %H%M%S')
				else:
					date_time = datetime.datetime.strptime(date, '%d%m%y')

			# dt_aware = timezone.localize(date_time)
			dt_aware = date_time.replace(tzinfo=timezone)
			dt_aware += datetime.timedelta(hours=6)
			self._date_time = dt_aware
		except Exception as e:
			print(str(e))
			raise TimeError
	'''latitude'''

	@property
	def lat(self):
		return self._lat

	@lat.setter
	def lat(self, arg):
		try:
			lat1, lat2 = arg
			if lat1 != "NA" and lat2 != "NA":
				self.get_latitude(lat1, lat2)
		except Exception as e:
			print(str(e))
			raise CoordinateError
	'''longitude'''

	@property
	def lon(self):
		return self._lon

	@lon.setter
	def lon(self, arg):
		try:
			lon1, lon2 = arg
			if lon1 != "NA" and lon2 != "NA":
				self.get_longitude(lon1, lon2)
		except Exception as e:
			print(str(e))
			raise CoordinateError

	'''speed'''
	@property
	def speed(self):
		return self._speed

	@speed.setter
	def speed(self, value):
		try:
			if value != "NA":
				self._speed = int(value)
		except Exception as e:
			print(str(e))
			raise StatisticError

	'''course'''
	@property
	def course(self):
		return self._course

	@course.setter
	def course(self, value):
		try:
			if value != "NA":
				converted_value =  int(value)
				if converted_value < 0 or converted_value > 360:
					raise SatelliteError
				self._course = converted_value
		except Exception as e:
			print(str(e))
			raise StatisticError

	'''alt'''

	@property
	def alt(self):
		return self._alt

	@alt.setter
	def alt(self, value):
		try:
			if value != "NA":
				self._alt = int(value)
		except Exception as e:
			print(str(e))
			raise StatisticError

	'''sats'''

	@property
	def sats(self):
		return self._sats

	@sats.setter
	def sats(self, value):
		try:
			if value != "NA":
				self._sats = int(value)
		except Exception as e:
			print(str(e))
			raise SatelliteError


	def save(self):
		# print("lon", self.lon, " lat", self.lat, "------------------")
		sh_req = ShortRequestSession.save_data(date_time=self.date_time, point=[self.lat, self.lon], speed=self.speed, course=self.course,
		                              alt=self.alt, sats=self.sats, black_box=self.black_box, imei=self.imei)
		return sh_req