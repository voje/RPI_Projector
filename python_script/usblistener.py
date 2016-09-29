import os
import getpass
import time

class UsbListener:
	def __init__(self, dirname='diapozitivi'):
		self.dirname = dirname
		self.dir_path = "./%s" % (dirname) #default dir path in project folder
		self.usbs_list = []
		self.change = False #flag that is set when new usb is inserted or ejected

	def find_usbs(self):
		uname = getpass.getuser()
		media_dir = "/media/%s" % (uname)
		new_usbs_list = os.listdir(media_dir)
		if len(new_usbs_list) != len(self.usbs_list):
			self.change = True
			self.usbs_list = new_usbs_list

	def new_usb(self):
		#Returns boolean if state has changes. Also changes flag after we checked the state.
		#"Was thre a change since I last called new_usb()?"
		res = self.change
		self.change = False
		return res

	def get_dir_path(self):
		if len(self.usbs_list) == 0:
			self.dir_path = None
			return

		#find the right USB
		for possible_path in self.usbs_list:
			path = "/media/%s/%s/%s" % (getpass.getuser(), possible_path, self.dirname)
			#wait for mount
			start_time = time.time()
			dtime = 0
			while (not os.path.isdir(path)) and (dtime < 5):
				dtime = time.time() - start_time
				#print "waiting for usb data...%f" % (dtime)
			if os.path.isdir(path):
				self.dir_path = path
				break
			else:
				print "could not find usb data, using default dir_path"
				self.dir_path = None

	def to_string(self):
		st = "UsbListener:\ndir_path: %s \nusbs_list: %s \nchange: %s \nUsbListener^" % (self.dir_path, self.usbs_list, self.change)
		return st

if __name__ == "__main__":
	print "Testing UsbListener:"
	ul = UsbListener("diapozitivi")
	ul.find_usbs()
	print ul.to_string()
	print ul.get_files_path()
