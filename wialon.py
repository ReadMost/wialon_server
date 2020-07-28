import datetime

from extended_request import ExtendedRequest
from my_lib import send_all_custom, save_logs
from short_request import ShortRequest
from wialon_base import WialonRequestBase
from exceptions import *


class WialonRequest(WialonRequestBase):
	def __init__(self, socket, clientAdress,  request, is_authorised):
		'''
		self.socket
		self.request
		self.packet_type
		self.msg
		self.crc
		'''
		super().__init__(socket, clientAdress, request)
		self.main_check(is_authorised)

	def main_check(self, is_authorised):
		if not is_authorised[0] and self.packet_type == "L":
			self.handle_login(is_authorised)
		elif not is_authorised[0]:
			raise CommonError(self.request, "Authentication is required")
		elif self.packet_type == "P":
			self.handle_ping()
		elif self.packet_type == "SD":
			self.handle_short_request()
		elif self.packet_type == "D":
			self.handle_extended_request()
		elif self.packet_type == "B":
			self.handle_black_box_request()
		else:
			send_all_custom(self.socket, "WARNING: Unhandled message")


	'''LOGIN'''
	def handle_login(self, is_authorised):
		login_arr = self.msg.split(";")
		protocol_version = login_arr[0]
		imei = login_arr[1]
		password = login_arr[2]

		# Checking the version 2.0
		try:
			if not float(protocol_version) == 2.0:
				send_all_custom(self.socket, "#AL#0")
			self.validate_crc()
			# todo: check the credentials to authentication
			if imei and password:
				is_authorised[0] = True
				send_all_custom(self.socket, "#AL#1")
			elif not password:
				send_all_custom(self.socket, "#AL#01")
		except CrcError:
			send_all_custom(self.socket, "#AL#10")
		except Exception as e:
			send_all_custom(self.socket, "ERROR: " + str(e))

	def handle_ping(self):
		send_all_custom(self.socket, "#AP#")

	'''SD request'''
	def handle_short_request(self):
		# Date;Time;Lat1;Lat2;Lon1;Lon2;Speed;Course;Alt;Sats;
		msg_splited = self.msg.split(";")
		try:
			self.validate_crc()
			short_req = ShortRequest(self.socket)
			short_req.date_time = msg_splited[0],msg_splited[1]
			short_req.lat = (msg_splited[2],msg_splited[3])
			short_req.lon = (msg_splited[4],msg_splited[5])
			short_req.speed = msg_splited[6]
			short_req.course = msg_splited[7]
			short_req.alt = msg_splited[8]
			short_req.sats = msg_splited[9]

			# Packet successfully registered.
			save_logs(self.clientAddress, str(short_req), dir="short_request_logs" )
			send_all_custom(self.socket, "#ASD#1")
		except TimeError:
			# Incorrect time.
			send_all_custom(self.socket, "#ASD#0")
		except CoordinateError:
			# Error receiving coordinates.
			send_all_custom(self.socket, "#ASD#10")
		except StatisticError:
			# Error receiving speed, course, or altitude.
			send_all_custom(self.socket, "#ASD#11")
		except SatelliteError:
			# Error receiving the number of satellites.
			send_all_custom(self.socket, "#ASD#12")
		except CrcError:
			# Checksum verification error.
			send_all_custom(self.socket, "#ASD#13")
		except IndexError:
			# Incorrect packet structure.
			send_all_custom(self.socket, "#ASD#-1")
		except Exception as e:
			# Incorrect packet structure.
			print(str(e) + " OTHER ERROR <<")
			send_all_custom(self.socket, "#ASD#-1")

	'''D request'''

	def handle_extended_request(self):
		# Date;Time;Lat1;Lat2;Lon1;Lon2;Speed;Course;Alt;Sats;HDOP;Inputs;Outputs;ADC;Ibutton;Params;
		msg_splited = self.msg.split(";")
		try:
			self.validate_crc()
			short_req = ExtendedRequest(self.socket)
			short_req.date_time = msg_splited[0], msg_splited[1]
			short_req.lat = (msg_splited[2], msg_splited[3])
			short_req.lon = (msg_splited[4], msg_splited[5])
			short_req.speed = msg_splited[6]
			short_req.course = msg_splited[7]
			short_req.alt = msg_splited[8]
			short_req.sats = msg_splited[9]
			short_req.hdop = msg_splited[10]
			short_req.inputs = msg_splited[11]
			short_req.outputs = msg_splited[12]
			short_req.adc = msg_splited[13]
			short_req.ibutton = msg_splited[14]
			short_req.parameters = msg_splited[15]

			# Packet successfully registered.
			save_logs(self.clientAddress, str(short_req), dir="extended_request_logs")
			send_all_custom(self.socket, "#AD#1")
		except TimeError:
			# Incorrect time.
			send_all_custom(self.socket, "#AD#0")
		except CoordinateError:
			# Error receiving coordinates.
			send_all_custom(self.socket, "#AD#10")
		except StatisticError:
			# Error receiving speed, course, or altitude.
			send_all_custom(self.socket, "#AD#11")
		except SatelliteError:
			# Error receiving the number of satellites.
			send_all_custom(self.socket, "#AD#12")
		except InOutError:
			# Error receiving the number of satellites.
			send_all_custom(self.socket, "#AD#13")
		except ADCError:
			# Error receiving the number of satellites.
			send_all_custom(self.socket, "#AD#14")
		except ParamsError:
			# Error receiving the number of satellites.
			send_all_custom(self.socket, "#AD#15")
		except CrcError:
			# Checksum verification error.
			send_all_custom(self.socket, "#AD#16")
		except IndexError:
			# Incorrect packet structure.
			send_all_custom(self.socket, "#AD#-1")
		except Exception as e:
			# Incorrect packet structure.
			print(str(e) + " OTHER ERROR <<")
			send_all_custom(self.socket, "#AD#-1")

	def handle_black_box_request(self):
		# Date;Time;Lat1;Lat2;Lon1;Lon2;Speed;Course;Alt;Sats;HDOP;Inputs;Outputs;ADC;Ibutton;Params;
		msg_spliteds = self.msg.split("|")
		try:
			self.validate_crc()
			total_num = 0
			bb_requests = []
			for msg_splited in msg_spliteds:
				if not msg_splited:
					continue
				try:
					msg_splited = msg_splited.split(";")
					short_req = ShortRequest(self.socket)
					short_req.date_time = msg_splited[0], msg_splited[1]
					short_req.lat = (msg_splited[2], msg_splited[3])
					short_req.lon = (msg_splited[4], msg_splited[5])
					short_req.speed = msg_splited[6]
					short_req.course = msg_splited[7]
					short_req.alt = msg_splited[8]
					short_req.sats = msg_splited[9]
					short_req.hdop = msg_splited[10]
					short_req.inputs = msg_splited[11]
					short_req.outputs = msg_splited[12]
					short_req.adc = msg_splited[13]
					short_req.ibutton = msg_splited[14]
					short_req.parameters = msg_splited[15]
					total_num+=1
					bb_requests.append(short_req)
				except:
					continue

			# Packet successfully registered.
			save_logs(self.clientAddress, str(bb_requests), dir="black_box_logs")
			send_all_custom(self.socket, f"#AB#{total_num}")
		except CrcError:
			# Checksum verification error.
			send_all_custom(self.socket, "#AB#")



