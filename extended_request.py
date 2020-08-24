from db.db_reflect import ExtendedPacketSession, ParamsSession
from exceptions import *
import datetime
class ExtendedRequest(object):
	def __init__(self, short_packet):

		self._hdop = None
		self._inputs = None
		self._outputs = None
		self._adc = ""
		self._ibutton = None
		self._parameters = None
		self.short_packet = short_packet

	def __repr__(self):
		result = ''
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


	def parse_params(self, params):
		result = []
		for param in params:
			splited_param = param.split(":")
			name, type_param, value = splited_param[0], int(splited_param[1]), splited_param[2]
			# try:
			# 	if type_param == 1:
			# 		value = int(value)
			# 	elif type_param == 2:
			# 		value = float(value)
			# 	elif type_param == 3:
			# 		pass
			# except:
			# 	continue
			result.append(dict(name=name,type=type_param, value=value))
		return result


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
			print(str(e), "-----------1---")
			raise ParamsError

	def save(self):
		# print("lon", self.lon, " lat", self.lat, "------------------")
		extended = ExtendedPacketSession.save_data(hdop=self.hdop, inputs=self.inputs,
		                                outputs=self.outputs, adc=self.adc, ibutton=self.ibutton, short_packet=self.short_packet)
		for param in self._parameters:
			ParamsSession.save_data(param['name'], param['type'], param['value'], extended.id)