import datetime
import threading
PACKET_END = b'\r\n'
import pickle
from pathlib import Path
from exceptions import *
buffer = b''
lock = threading.Lock()
class MyThread(threading.Thread):
	def __init__(self):
		super().__init__()
		self.buffer = b''

	def recv_custom(self, ssock, is_pickle=False):
		# lock.acquire()
		buffer = self.buffer
		while True:
			data = ssock.recv(1024)
			if not data:
				break
			buffer += data

			if PACKET_END not in buffer:
				continue

			message, ignored, buffer = buffer.partition(PACKET_END)
			self.buffer = buffer
			# lock.release()
			if is_pickle:
				return pickle.loads(message)
			return message.decode()

	def send_all_custom(self, ssock, mess):
		mess = bytes(mess, 'UTF-8')
		sending_string = b"".join([mess, PACKET_END])
		ssock.sendall(sending_string)

	def save_logs(self, clientAddress, msg, time=datetime.datetime.now(), dir=""):
		if dir:
			Path(dir).mkdir(parents=True, exist_ok=True)
		if dir[-1] != '/':
			dir += '/'
		if not msg:
			msg = "NO LOGS"
		with open(dir + clientAddress[0] + ":" + str(clientAddress[1]) + ".txt", "a+") as f:
			f.write(str(time) + " => " + msg + "\n")



def recv_custom(ssock, is_pickle=False):
	global buffer
	while True:
		data = ssock.recv(1024)
		if not data:
			break
		buffer += data

		if PACKET_END not in buffer:
			continue

		message, ignored, buffer = buffer.partition(PACKET_END)

		if is_pickle:
			return pickle.loads(message)
		return message.decode()

def send_all_custom(ssock, mess):
	mess = bytes(mess, 'UTF-8')
	sending_string = b"".join([mess, PACKET_END])
	ssock.sendall(sending_string)

def save_logs(clientAddress, msg, time=datetime.datetime.now(), dir=""):
	if dir:
		Path(dir).mkdir(parents=True, exist_ok=True)
	if dir[-1] != '/':
		dir += '/'
	with open(dir + clientAddress[0] + ":" + str(clientAddress[1]) + ".txt", "a+") as f:
		f.write(str(time) + " => " + msg + "\n")

