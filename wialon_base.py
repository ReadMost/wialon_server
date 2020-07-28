import binascii
import zlib

import pynmea2

from statics import *
from exceptions import *

class WialonRequestBase:
	def __init__(self, socket ,clientAddress, request):
		self.socket = socket
		self.clientAddress = clientAddress
		self.request = request
		self.packet_type = None
		self.msg = None
		self.crc = None

		# todo: remove in production
		# if not DEBUG:
		# 	self.decompress_request()
		self.parse_request()
		# self.validate_crc()

	def __repr__(self):
		return self.packet_type + " - " + self.msg

	def parse_request(self):
		divided_request = self.request.split("#")
		self.packet_type = divided_request[1]
		msg = divided_request[-1].split(";")
		crc_hex = msg.pop()
		if crc_hex:
			crc = int(crc_hex, 16)
			self.crc = hex(crc)
		self.msg = ";".join(msg) + ";"

	def decompress_request(self):
		try:
			mess = bytes(self.request[6:], 'UTF-8')
			new_request = zlib.decompress(binascii.unhexlify(mess))
			self.request = new_request.decode()
		except Exception as e:
			raise DecompressError(self.request)

	def GetCrc16(strHexData):
		# fcs = int("FFFF",16)
		fcs = 0
		i = 0
		while i < len(strHexData):
			strHexNumber = strHexData[i:i + 2]
			# print("str "+strHexNumber)
			intNumber = int(strHexNumber, 16)
			crc16tabIndex = (fcs ^ intNumber) & int("0xFF", 16)
			fcs = (fcs >> 8) ^ crc16_table[crc16tabIndex]
			i = i + 2
		return fcs

	def validate_crc(self):
		def GetCrc16(strHexData):
			# fcs = int("FFFF",16)
			fcs = 0
			i = 0
			while i < len(strHexData):
				strHexNumber = strHexData[i:i + 2]
				# print("str "+strHexNumber)
				intNumber = int(strHexNumber, 16)
				crc16tabIndex = (fcs ^ intNumber) & int("0xFF", 16)
				fcs = (fcs >> 8) ^ crc16_table[crc16tabIndex]
				i = i + 2
			return fcs

		toHex = lambda x: "".join([hex(ord(c))[2:].zfill(2) for c in x])
		calculated_crc = hex(GetCrc16(toHex(self.msg)))
		if not self.crc == calculated_crc:
			print("Given CRC: ",self.crc, " == Calculated: ", calculated_crc)
			raise CrcError(self.request)



	def parse_coord(self, msg):

		'''
		:param msg:
		:return:
		{
			'date': datetime.datetime(2017, 9, 11, 14, 38, 54),
			'coord': [53.905793333333335, 27.456953333333335]
		}
		'''
		parsed_coord = pynmea2.parse(msg)
		return dict(date=parsed_coord.datetime, coord=[parsed_coord.latitude, parsed_coord.longitude])

