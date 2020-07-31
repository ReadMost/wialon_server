

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
	def __str__(self):
		return "CoordinateError"

class TimeError(Exception):
	def __str__(self):
		return "TimeError"

class StatisticError(Exception):
	def __str__(self):
		return "StatisticError"

class SatelliteError(Exception):
	def __str__(self):
		return "SatelliteError"

class InOutError(Exception):
	def __str__(self):
		return "InOutError"

class ADCError(Exception):
	def __str__(self):
		return "ADCError"
class ParamsError(Exception):
	def __str__(self):
		return "ParamsError"