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
client.connect((CLIENT_SERVER, PORT))
count = 0
while True:
	# if count < 5 and count != 0:
	# 	out_data = ''
	# 	count += 1
	# elif count == 0:
	# 	out_data = "#L#2.0;IMEI;Password;"
	# 	count = 1
	# else:
	# 	out_data = input()
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

#L#2.0;Time;Password;
#c#2.0;IMEI;;2d49
#SD#NA;NA;NA;N;NA;E;12;NA;NA;2;
#D#121112;123212;NA;NA;NA;NA;NA;NA;NA;NA;2.2;0101;0101;ADC;Ibutton;name1:1:Value,name2:2:123.123,name3:3:Value;
#B#270720;210011;5205.6137;N;07015.5806;E;10;86;3622;18;NA;NA;NA;;NA;ign:1:1|270720;210041;5205.6171;N;07015.6478;E;10;86;3620;18;NA;NA;NA;;NA;ign:1:1|270720;210111;5205.6206;N;07015.7147;E;10;85;3621;18;NA;NA;NA;;NA;ign:1:1|270720;210141;5205.6238;N;07015.7814;E;10;84;3632;18;NA;NA;NA;;NA;ign:1:1|
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225217;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225247;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225317;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225347;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225355;NA;NA;NA;NA;NA;NA;NA;NA|270720;225418;NA;NA;NA;NA;NA;NA;NA;NA|270720;225837;NA;NA;NA;NA;NA;NA;NA;NA|270720;231437;NA;NA;NA;NA;NA;NA;NA;NA|
#D#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;count1:1:564,fuel:2:45.8,hw:3:V4.5,SOS:1:1;

#B#300720;115640;5205.9761;N;07020.9050;E;24;360;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115652;5206.0131;N;07020.9089;E;20;5;3760;10;NA;NA;NA;;NA;ign:1:1|300720;115706;5206.0558;N;07020.9112;E;24;358;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115710;5206.0699;N;07020.9112;E;24;0;3761;10;NA;NA;NA;;NA;ign:1:1|