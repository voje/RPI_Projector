import os
import getpass
import time

class UsbListener:
	def __init__(self, dirname='diapozitivi', logger=None):
		self.dirname = dirname
		self.default_dir_path = "./%s" % (dirname) #default dir path in project folder
                self.usb_dir_path = ""
		self.lg = logger

	def find_usb(self):
		uname = getpass.getuser()

		media_dir = "/media/%s" % (uname)
                while not os.path.isdir(media_dir):
                    time.sleep(3)
                found_media_usb = False
                while not found_media_usb:
                    usb_names = os.listdir(media_dir)
                    for un in usb_names:
                        tmp_dir = "/media/%s/%s/%s" % (uname, un, self.dirname)
                        if os.path.isdir(tmp_dir):
                            self.usb_dir_path = tmp_dir
                            found_media_usb = True
                            break
                    time.sleep(3)

                self.lg.log_event( "usblistener.py", "detected USB with media: %s" % (self.usb_dir_path) )

if __name__ == "__main__":
	print "Testing UsbListener:"
	ul = UsbListener("diapozitivi")
	ul.find_usb()
