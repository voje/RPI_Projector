# Core application for slideshow_plus.
import getpass
from os import listdir
from os.path import isfile, join


class Core():
    def __init__(self):
        self.files = {}
        self.current_file = {}

    def find_usb(self):
        # Loops through mounted USBS,
        # Returns path to files folder or None

        # media_dir = "/media/{}".format(getpass.getuser())
        media_dir = "/home/kristjan/Desktop/test/"
        test = [join(media_dir, x) for x in listdir(media_dir) if not isfile(join(media_dir, x))]
        print(test)


if __name__ == "__main__":
    core = Core()
    core.find_usb()
