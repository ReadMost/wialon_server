from exceptions import *
import datetime
class ExtendedRequest(object):
	def __init__(self, socket):
		self.socket = socket
		self._date_time = None
		self._lat = None
		self._lon = None
		self._speed = None
		self._course = None
		self._alt = None
		self._sats = None
		self._hdop = None
		self._inputs = None
		self._outputs = None
		self._adc = ""
		self._ibutton = None
		self.parameters = None

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
		if self._hdop:
			result += "_hdop:" + str(self._hdop) + ";"
		if self._inputs:
			result += "_inputs:" + str(self._inputs) + ";"
		if self._outputs:
			result += "_outputs:" + str(self._outputs) + ";"
		if self._adc:
			result += "_adc:" + self._adc + ";"
		if self._ibutton:
			result += "_ibutton:" + str(self._ibutton) + ";"
		if self.parameters:
			result += "parameters:" + str(self.parameters) + ";"
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

	def parse_params(self, params):
		result = []
		for param in params:
			splited_param = param.split(":")
			name, type_param, value = splited_param[0], int(splited_param[1]), splited_param[2]
			try:
				if type_param == 1:
					value = int(value)
				elif type_param == 2:
					value = float(value)
				elif type_param == 3:
					pass
			except:
				continue
			result.append(dict(name=name,type=type_param, value=value))
		return result

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
			self._date_time = date_time
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
				if converted_value < 0 or converted_value > 359:
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

	'''hdop'''

	@property
	def hdop(self):
		return self._hdop

	@hdop.setter
	def hdop(self, value):
		try:
			if value != "NA":
				self._hdop = float(value)
		except Exception as e:
			print(str(e))
			raise SatelliteError

	'''inputs'''

	@property
	def inputs(self):
		return self._inputs

	@inputs.setter
	def inputs(self, value):
		try:
			if value != "NA":
				self._inputs = int(value)
		except Exception as e:
			print(str(e))
			raise InOutError

	'''outputs'''

	@property
	def outputs(self):
		return self._outputs

	@outputs.setter
	def outputs(self, value):
		try:
			if value != "NA":
				self._outputs = int(value)
		except Exception as e:
			print(str(e))
			raise InOutError

	'''adc'''

	@property
	def adc(self):
		return self._adc

	@adc.setter
	def adc(self, value):
		try:
			if value != "":
				self._adc = value
		except Exception as e:
			print(str(e))
			raise ADCError

	'''ibutton'''

	@property
	def ibutton(self):
		return self._ibutton

	@ibutton.setter
	def ibutton(self, value):
		try:
			if value != "NA":
				self._alt = value
		except Exception as e:
			print(str(e))
			raise StatisticError

	'''parameters'''

	@property
	def parameters(self):
		return self._parameters


	@parameters.setter
	def parameters(self, value):
		try:
			if value:
				self._parameters = self.parse_params(value.split(","))
		except Exception as e:
			print(str(e))
			raise ParamsError