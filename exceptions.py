

class CrcError(Exception):
	def __init__(self, request, message = "CRC16 check is failed"):
		self.request = request
		self.message = message

	def __str__(self):
		return f'CrcError {self.request} -> {self.message}'

class DecompressError(Exception):
	def __init__(self, request, message="decompress error"):
		self.request = request
		self.message = message

	def __str__(self):
		return f'DecompressError: {self.request} -> {self.message}'

class CommonError(Exception):
	def __init__(self, request, message):
		self.request = request
		self.message = message

	def __str__(self):
		return f'{self.request} -> {self.message}'

class CoordinateError(Exception):
	pass

class TimeError(Exception):
	pass

class StatisticError(Exception):
	pass

class SatelliteError(Exception):
	pass

class InOutError(Exception):
	pass

class ADCError(Exception):
	pass
class ParamsError(Exception):
	pass