# -*- coding: utf-8 -*-
import socket
import sys

class TcpClient:
	def __init__(self, logger=None):
		self.ip = "192.168.1.143"
		#self.ip = "127.0.0.1" #for testing
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

		sock = socket.socket()
		sock.connect((self.ip, self.port))
		f = sock.makefile()

		#request
		data = self.commands[command]
		f.write(data)
		f.flush()

		eslf.lg.log_event("tcp_client.py", "commnd %s sent" % (command) )

		#response ... maybe this is causing the blockage
		"""
		n1 = 9	#length of first response (PJLINK 0)
		n2 = 9	#actually they can be longer but ok
		n = n1 + n2
		r_data = f.read(n).decode('utf-8')	
		self.lg.log_event("C", r_data)
		"""

		#close socket
		f.close()
		sock.close()

if __name__ == "__main__":
	tc = TcpClient()
	tc.send_command("query")
