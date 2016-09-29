import os

class LoggerWrapper:
	def __init__(self, l_on=True):
		self.script_path="/home/pi/git/RPI_Projector/logging/log_event.sh"
		self.logging_on=l_on

	def log_event(self, msg_type, msg):
		if not self.logging_on:
			return
		tmp=""+self.script_path+" '"+msg_type+"' '"+msg+"'"
		os.system(tmp)

if __name__ == "__main__":
	l = LoggerWrapper()
	l.log_event("Z", "derp derp")