import sys
sys.path.append('/home/kristjan/git/RPI_Projector/python_script')
from presenter import *
import time

pr = Presenter(5, "../diapozitivi")

while True:
	s = pr.fifo.readline()	
	if s != "":
		print s
	time.sleep(5)	#the order stays correct, I would suggest 0.5 second sleep