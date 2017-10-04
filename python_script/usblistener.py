import os
import getpass
import time

class UsbListener:
	def __init__(self, dirname='diapozitivi', logger=None):
		self.dirname = dirname
		self.dir_path = "./%s" % (dirname) #default dir path in project folder
		self.usbs_list = []
		self.change = False #flag that is set when new usb is inserted or ejected
		self.lg = logger

	def find_usbs(self):
		uname = getpass.getuser()
		media_dir = "/media/%s" % (uname)
                if not os.path.isdir(media_dir):
                    return
		new_potential_usbs_list = os.listdir(media_dir)
                #only include those with a "self.dirname"
                new_usbs_list = []
                for pot in new_potential_usbs_list:
                    path = "/media/%s/%s" % (uname, pot)
                    if os.path.isdir(path):
                        new_usbs_list += [pot]

		if new_usbs_list != self.usbs_list:
			self.change = True
			self.usbs_list = new_usbs_list
                        self.lg.log_event( "usblistener.py", "usb_list updated: %s" % (self.usbs_list) )

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
			#print "Possible path: %s" % (path)
			#wait for mount
			start_time = time.time()
			dtime = 0
			while (not os.path.isdir(path)) and (dtime < 1):
				dtime = time.time() - start_time
				#print "waiting for usb data...%f" % (dtime)
			if os.path.isdir(path):
				self.dir_path = path
				break
		else:
			self.lg.log_event( "usblistener.py", "could not find dir_path in list %s; using default dir_path" % (self.usbs_list) )
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
