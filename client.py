import socket
import threading

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

#L#2.0;Fuel;Password;
#L#2.0;205005895;Password;
#O#
#c#2.0;IMEI;;2d49
#SD#NA;NA;NA;N;NA;E;12;NA;NA;2;
#D#121112;123212;NA;NA;NA;NA;NA;NA;NA;NA;2.2;0101;0101;ADC;Ibutton;name1:1:Value,name2:2:123.123,name3:3:Value;
#B#270720;210011;5205.6137;N;07015.5806;E;10;86;3622;18;NA;NA;NA;;NA;ign:1:1|270720;210041;5205.6171;N;07015.6478;E;10;86;3620;18;NA;NA;NA;;NA;ign:1:1|270720;210111;5205.6206;N;07015.7147;E;10;85;3621;18;NA;NA;NA;;NA;ign:1:1|270720;210141;5205.6238;N;07015.7814;E;10;84;3632;18;NA;NA;NA;;NA;ign:1:1|
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225217;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225247;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225317;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225347;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225355;NA;NA;NA;NA;NA;NA;NA;NA|270720;225418;NA;NA;NA;NA;NA;NA;NA;NA|270720;225837;NA;NA;NA;NA;NA;NA;NA;NA|270720;231437;NA;NA;NA;NA;NA;NA;NA;NA|

#D#010820;024011;5353.2286;N;06208.2994;E;0;280;226.000000;8;0.940000;2;0;NA,11.918000;NA;fuel2:1:927,fuel3:1:843,temp2:1:20,temp3:1:20,param1:1:4,param2:1:8,param3:1:0,custom:2:242.040816,custom1:2:269.333333,fuel level:2:511.374150,engine operation:2:1.000000;
#D#010820;105052;5356.7442;N;06208.5618;E;8;86;204.000000;19;0.610000;2;0;NA,11.623000;NA;fuel2:1:524,fuel3:1:542,temp2:1:44,temp3:1:40,param1:1:1048576,param2:1:11,param3:1:8,custom:2:139.714286,custom1:2:127.826087,fuel level:2:267.540373,engine operation:2:1.000000;
#D#240820;130139;5353.5815;N;06207.9422;E;48;69;0.000000;20;NA;128;NA;17.285000;NA;msg_type:3:A,proto:3:FLEX1.0,msg_number:1:329118,event_code:1:5893,status:1:0,modules_st:1:169,modules_st2:1:0,gsm:1:11,nav_rcvr_state:1:1,valid_nav:1:1,sats:1:20,mileage:2:9257.356445,pwr_ext:2:14.965000,pwr_int:2:3.667000,engine_hours:2:446.095556,rs485fuel_level1:1:555,rs485fuel_level2:1:65530,fuel level:2:62.547771,voltage:2:14.965000,engine operation:2:1.000000
#B#300720;115640;5205.9761;N;07020.9050;E;24;360;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115652;5206.0131;N;07020.9089;E;20;5;3760;10;NA;NA;NA;;NA;ign:1:1|300720;115706;5206.0558;N;07020.9112;E;24;358;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115710;5206.0699;N;07020.9112;E;24;0;3761;10;NA;NA;NA;;NA;ign:1:1|