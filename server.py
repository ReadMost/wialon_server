import socket, threading
from statics import *
from termcolor import colored, cprint
from my_lib import MyThread
from wialon import WialonRequest
# FF76007801258CCB0AC24010043F26D77599DE9931ECF4C9D7351EF2050145024625F8FF9818EA540DD5CDB9290A41215CAB57BABA65AB652FEC28A55564B35A8517CA828AB02532FE86242BEC0E1C1FAF4020DD3EC33C4C5142330CBE1C79FA6E9BC6F33DDFA7346E8AD8B9A7FEDAAF1DED78D21FEF7522F7

class ClientThread(MyThread):
	def __init__(self, clientAddress, clientsocket):
		super().__init__()
		self.csocket = clientsocket
		self.is_authorised = [False]
		self.clientAddress = clientAddress
		print("New connection added: ", clientAddress)

	def run(self):


			while True:
				try:
					msg = ''
					msg = self.recv_custom(self.csocket)
					if msg is None:
						raise OSError
					# print(msg,  "<<<")
					self.save_logs(self.clientAddress, msg, dir = "pure_logs")
					if msg == 'bye':
						break
					request = WialonRequest(self.csocket, self.clientAddress,  msg, self.is_authorised)
					# self.send_all_custom(self.csocket, msg)

				except self.csocket.error:
					print("\033[1;35;40m",  str(socket.error))
					cprint(str(socket.error), "yellow", "on_grey")
					self.save_logs(self.clientAddress, "ERROR!!! " + str(socket.error), dir = "error_logs")
				except OSError as e:
					print(str(e), "-------------")
					cprint(str(self.clientAddress) + " has gone", "red", "on_grey")
					break

				except Exception as e:
					cprint(str(e), "magenta", "on_cyan")
					self.send_all_custom(self.csocket, "ERROR: " + str(e))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER, PORT))
# print("Server started")
print("Waiting for client request..")
while True:
	server.listen(5)
	clientsock, clientAddress = server.accept()
	newthread = ClientThread(clientAddress, clientsock)
	newthread.start()
