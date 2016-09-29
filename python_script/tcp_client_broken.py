# -*- coding: utf-8 -*-
import socket
import sys

class tcp_client:
	def __init__(self):
		#self.tcp_ip = "127.0.0.1"
		self.tcp_ip = "192.168.1.143"
		self.tcp_port = 41794
		self.buffer_size = 1024	#bytes
		self.messages = {
			"on": '%1POWR 1\r',
			"off": '%1POWR 0\r',
			"query": '%1'+'POWR'+' '+'?'+'\r',
			"gibberish": 'asdf',
			"empty": ''
		}

	def send_message(self, message):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.tcp_ip, self.tcp_port))
		f = s.makefile(mode='rw')
		f.write(message)
		f.flush()

		data = f.read(4)
		#data += f.read(2 + 4 + 1 - len(data))
		data = data.decode('utf-8')
		f.close()
		s.close()
		print "response: "
		print type(data)
		print sys.getsizeof(data)
		print "len: ", len(data)
		print data
		print "#####################"

if __name__ == "__main__":
	t = tcp_client()
	t.send_message(t.messages["query"])
