# -*- coding: utf-8 -*-
import socket
import sys
import time

class TcpClient:
	def __init__(self, logger=None):
		#self.ip = "192.168.1.143"
		self.ip = "127.0.0.1" #for testing
		self.port = 4352
		self.commands = {
			"on": '%1POWR 1\r',
			"off": '%1POWR 0\r',
			"query": '%1POWR ?\r'
		}
		self.lg = logger

	def send_command(self, command):
		self.lg.log_event("tcp_client.py", "sending command: %s" % (command) );
		#pj_client has a mute option
		if command == "mute":
			return

		### official python tcp/ip
		BUFFER_SIZE = 1024

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setblocking(0)
		s.settimeout(2)
		s.connect((self.ip, self.port))
		s.send(self.commands[command])
		data = s.recv(BUFFER_SIZE)
		s.close()

		self.lg.log_event("tcp_client.py", "response: %s" % (data) );
		###

		#my socket attempt
		"""
		sock = socket.socket()
		sock.connect((self.ip, self.port))
		f = sock.makefile()

		#request
		data = self.commands[command]
		f.write(data)
		f.flush()
		""" 
		#response ... maybe this is causing the blockage
		"""
		n1 = 9	#length of first response (PJLINK 0)
		n2 = 9	#actually they can be longer but ok
		n = n1 + n2
		r_data = f.read(n).decode('utf-8')	
		self.lg.log_event("C", r_data)
		"""

		"""
		#close socket
		f.close()
		sock.close()
		"""

if __name__ == "__main__":
	tc = TcpClient()
	while (true):
		time.sleep(2)	
		tc.send_command("on")

