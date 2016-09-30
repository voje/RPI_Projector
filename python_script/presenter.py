#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
from usblistener import UsbListener

class MemoryList:
	def __init__(self, size):
		self.size = size
		self.mem_list = []
		self.mem_index = -1

	def append(self, item):
		#entering a new number sets the index to the last entered file
		self.mem_list.append(item)
		if len(self.mem_list) > self.size:
			self.mem_list.pop(0)
		self.mem_index = len(self.mem_list)-1

	def flush(self):
		self.mem_list = []
		mem_index = -1

	def get_file_index(self):
		if self.mem_index == -1:
			return -1
		if self.mem_index >= len(self.mem_list):
			return -1
		return self.mem_list[self.mem_index]

	def increment_index(self):
		if len(self.mem_list) == 0:
			return
		last_index = len(self.mem_list)-1
		self.mem_index+=1
		if self.mem_index > last_index:
			self.mem_index = last_index

	def decrement_index(self):
		if len(self.mem_list) == 0:
			return
		self.mem_index-=1
		if self.mem_index < 0:
			self.mem_index = 0

	def to_string(self):
		string = "MemoryList:\n"
		for (i, element) in enumerate(self.mem_list):
			if i == self.mem_index:
				string += "<%s>, " % (element)
			else:
				string += "%s, " % (element)
		return string

class Presenter:
	def __init__(self, mem_size, dirname="diapozitivi", logger=None):
		self.mem_list = MemoryList(mem_size)
		self.dirname = dirname
		self.script_path = os.path.dirname(os.path.realpath(__file__))
		self.files_path = ""
		self.get_default_file_path()
		self.files_list = []
		self.get_files_list()
		self.current_file_index = 0					#displayed file
		self.ul = UsbListener(self.dirname)
		self.input_buffer = ""
		self.fifo_path = "%s/ir.fifo" % (self.script_path)
		if not os.path.exists(self.fifo_path):
			os.mkfifo(self.fifo_path)
		self.lg=logger

	def get_default_file_path(self):
		self.files_path = "%s/%s" % (self.script_path, self.dirname)

	def get_files_list(self, path=None):
		if path == None:
			self.get_default_file_path()
		else:
			self.files_path = path
		self.files_list = os.listdir(self.files_path)
		#sort the list
		tuples = [(self.extract_number(x),x) for x in self.files_list]
		tuples.sort(key=lambda tup: tup[0])
		self.files_list = [x[1] for x in tuples]
		#flush memory (don't want wild indexes)
		self.mem_list.flush()
		self.set_cfi(0)

	def set_cfi(self, index):
		if index < 0:
			return
		self.current_file_index = index

	def next_file(self):
		num_files = len(self.files_list)
		if self.current_file_index >= (num_files-1):
			self.current_file_index = (num_files-1)
			return
		self.current_file_index += 1

	def prev_file(self):
		if self.current_file_index <= 0:
			self.current_file_index = 0
			return
		self.current_file_index -= 1

	def find_file_index(self, input_number):
		#file number is 12_Name_of_song, file index is the position in a directory
		res = -1
		for (i, name) in enumerate(self.files_list):
			file_number = self.extract_number(name)
			#print file_number
			if file_number == input_number:
				res = i
				break
		#print "Found index of file: %d --> index: %d" % (input_number, res)
		return res

	def extract_number(self, file_name):
		#get index out of file name	
		res = re.search('[0-9]+', file_name)
		num = res.group(0)
		no_lead_zeros = num.lstrip("0")
		if len(no_lead_zeros) == 0:
			return 0
		return int(no_lead_zeros)

	def display_file(self, blank=False):
		server = "my_server"
		file = self.files_list[self.current_file_index]
		if blank:
			file = self.files_list[0]
		file_path = self.files_path + "/" + file
		#fullscreen mode
		try:
			pass
			#os.system("xpdf -fullscreen -remote %s '%s' &" % (server, file_path))
			#window mode
			#os.system("xpdf -remote %s '%s' &" % (server, file_path))
		except:
			pass
		tmp="displaying file: [%d]%s" % (self.current_file_index, file)
		self.lg.log_event("presenter.py", tmp)
		self.lg.log_event("", "")

	def to_string(self):
		st = "Presenter: \n%s \ndirname: %s \nfiles_list(%d): %s \ncurrent_file_index: %s \n%s \ninput_buffer: %s" % \
			(self.mem_list.to_string(), self.dirname, len(self.files_list), self.files_list[0:20], self.current_file_index, self.ul.to_string(), self.input_buffer)
		return st

if __name__ == "__main__":
	print "Running tests:"

	print "Presenter test:"
	p = Presenter(5, "diapozitivi")
	print p.to_string()

	print "Testing response to USB insertion."
	while True:
		p.ul.find_usbs()
		if p.ul.new_usb():
			print "Bang!"
		time.sleep(0.5)

	"""
	print "get_indexl test:"
	print p.get_index("12asdf")
	print p.get_index("012_asdf")	
	print p.get_index("120_asdf")	
	print p.get_index("120asdf")
	print p.get_index("_1_20asdf")
	print p.get_index("0012_0asdf")
	print p.get_index("34 testfile 32 txt")
	"""


	"""
	print "MemoryList test:"

	m = MemoryList(5)
	m.append("banana")
	m.append("jabolko")
	m.append("hruška")
	m.append("pomaranča")
	m.append("limona")
	m.append("grenivka")
	m.append("marelica")
	print m.to_string()

	m.decrement_index()
	m.decrement_index()
	print m.to_string()

	m.increment_index()
	m.increment_index()
	m.increment_index()
	m.increment_index()
	print m.to_string()

	m.decrement_index()
	m.decrement_index()
	m.decrement_index()
	m.decrement_index()
	m.decrement_index()
	m.decrement_index()
	print m.to_string()

	m.increment_index()
	print m.to_string()
	"""
