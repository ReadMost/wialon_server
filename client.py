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

#L#2.0;205005896;Password;
#L#2.0;fuel;Password;
#OL#["fuel", "me", "second"];
#c#2.0;IMEI;;2d49
#SD#NA;NA;NA;N;NA;E;12;NA;NA;2;
#D#121112;123212;NA;NA;NA;NA;NA;NA;NA;NA;2.2;0101;0101;ADC;Ibutton;name1:1:Value,name2:2:123.123,name3:3:Value;
#B#270720;210011;5205.6137;N;07015.5806;E;10;86;3622;18;NA;NA;NA;;NA;ign:1:1|270720;210041;5205.6171;N;07015.6478;E;10;86;3620;18;NA;NA;NA;;NA;ign:1:1|270720;210111;5205.6206;N;07015.7147;E;10;85;3621;18;NA;NA;NA;;NA;ign:1:1|270720;210141;5205.6238;N;07015.7814;E;10;84;3632;18;NA;NA;NA;;NA;ign:1:1|
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;
#B#270720;225122;5205.3320;N;07016.9648;E;7;277;3726;11;NA;NA;NA;;NA;ign:1:1|270720;225147;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225217;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225247;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225317;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225347;5205.3322;N;07016.9620;E;0;280;3722;11;NA;NA;NA;;NA;ign:1:1|270720;225355;NA;NA;NA;NA;NA;NA;NA;NA|270720;225418;NA;NA;NA;NA;NA;NA;NA;NA|270720;225837;NA;NA;NA;NA;NA;NA;NA;NA|270720;231437;NA;NA;NA;NA;NA;NA;NA;NA|


#D#140820;034656;5352.1282;N;06202.7792;E;9;263;211.000000;18;0.580000;2;0;NA,15.976000;NA;fuel2:1:660,fuel3:1:674,temp2:1:20,temp3:1:20,param1:1:1048576,param2:1:10,param3:1:8,engine operation:2:1.000000,fuel level:2:355.377155,custom:2:174.687500,custom1:2:180.689655;
#D#140820;034656;5352.1282;N;06202.7792;E;9;263;211.000000;18;0.580000;2;0;NA,15.976000;NA;fuel2:1:660,fuel3:1:674,temp2:1:20,temp3:1:20,param1:1:1048576,param2:1:10,param3:1:8,engine operation:2:1.000000,fuel level:2:355.377155,custom:2:174.687500,custom1:2:180.689655;
#B#300720;115640;5205.9761;N;07020.9050;E;24;360;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115652;5206.0131;N;07020.9089;E;20;5;3760;10;NA;NA;NA;;NA;ign:1:1|300720;115706;5206.0558;N;07020.9112;E;24;358;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115710;5206.0699;N;07020.9112;E;24;0;3761;10;NA;NA;NA;;NA;ign:1:1|


'''Version 1'''
#L#VERSION1;NA
#D#280820;120556;5356.0228;N;06204.6092;E;0;348;0.000000;19;NA;128;NA;0.219000;NA;msg_type:3:A,proto:3:FLEX1.0,msg_number:1:343808,event_code:1:5899,status:1:0,modules_st:1:41,modules_st2:1:0,gsm:1:9,nav_rcvr_state:1:1,valid_nav:1:1,sats:1:19,mileage:2:9770.639648,pwr_ext:2:12.938000,pwr_int:2:3.620000,engine_hours:2:477.134167,rs485fuel_level1:1:539,rs485fuel_level2:1:65530,fuel level:2:60.509554,voltage:2:12.938000,engine operation:2:0.000000
#B#300720;115640;5205.9761;N;07020.9050;E;24;360;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115652;5206.0131;N;07020.9089;E;20;5;3760;10;NA;NA;NA;;NA;ign:1:1|300720;115706;5206.0558;N;07020.9112;E;24;358;3759;10;NA;NA;NA;;NA;ign:1:1|300720;115710;5206.0699;N;07020.9112;E;24;0;3761;10;NA;NA;NA;;NA;ign:1:1
#D#130820;125929;5351.6595;N;06202.5164;E;5;98;204.000000;18;0.560000;2;0;NA,15.964000;NA;fuel2:1:285,fuel3:1:289,temp2:1:25,temp3:1:28,param1:1:1048576,param2:1:11,param3:1:7,engine operation:2:1.000000,fuel level:2:140.750000,custom:2:70.000000,RAUAN:2:70.750000