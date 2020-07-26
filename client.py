import socket
from statics import *
from my_lib import recv_custom, send_all_custom

def get_crc(msg):
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
	return hex(GetCrc16(toHex(msg)))
'''
REFERENCES:
   https://crccalc.com/ - from crc conversion check
   https://www.rapidtables.com/convert/number/decimal-to-hex.html?x=45695  -  conversion the decimal to hex online
   https://github.com/croja/wialon_ips/blob/master/wialon_ips.py - tests here
'''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
while True:
	out_data = input()
	# todo: uncomment in debug mode
	if DEBUG:
		crc = get_crc(out_data.split("#")[-1])
		out_data += crc
	send_all_custom(client, out_data)
	if out_data == 'bye':
		break
	print(recv_custom(client))
client.close()

#L#2.0;IMEI;Password;
#c#2.0;IMEI;;2d49
#SD#NA;NA;NA;N;NA;E;12;NA;NA;2;
#D#121112;123212;NA;NA;NA;NA;NA;NA;NA;NA;2.2;0101;0101;ADC;Ibutton;name1:1:Value,name2:2:123.123,name3:3:Value;

