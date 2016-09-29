import os
import presenter
import tcp_client
import pj_client
import time
import logger_wrapper

if __name__ == "__main__":
	lg = logger_wrapper.LoggerWrapper(l_on=False)
	lg.log_event("main.py", "Starting powerpoint script.")
	pr = presenter.Presenter(20, logger=lg)
	#tc = tcp_client.TcpClient()
	tc = pj_client.PjClient()

	print "Client ready."

	#initially display file 0
	pr.ul.find_usbs()
	if pr.ul.new_usb():
		print "USB initially present."
		lg.log_event("main.py", "USB initially present.")
		pr.ul.get_dir_path()
		pr.get_files_list(pr.ul.dir_path)
	pr.display_file()

	while True:
		time.sleep(0.3)

		#check if new USB was inserted
		pr.ul.find_usbs()
		if pr.ul.new_usb():
			lg.log_event("main.py", "USB change detected.")
			pr.ul.get_dir_path()
			print "usb dir path: %s" % ( pr.ul.dir_path )
			pr.get_files_list(pr.ul.dir_path)
			#display first file from storage
			pr.display_file()

		#check fifo for new input from ir remote
		#FIFO = os.open(pr.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
		FIFO = os.open(pr.fifo_path, 'r', 0)
		read_done = False
		while not read_done:
			try:
				st = os.read(FIFO, 200)
				read_done = True
			except:
				print "FAIL"
				pass
		os.close(FIFO)
		if st == "":
			continue
			lg.log_event("main.py", "FIFO gave empty string.")
		#remove newline
		st = st[0:-1]
		lg.log_event("main.py", "FIFO gave string: "+st)

		if st.isdigit():
			pr.input_buffer += st
		elif st == "KEY_O":
			#since there is a blank (file 0) option, we need to re-display our current file
			pr.display_file()
			try:
				tc.send_command("on")
			except Exception:
				lg.log_event("main.py", "projector power on failed")
		elif st == "KEY_P":
			try:
				tc.send_command("off")
			except Exception:
				lg.log_event("main.py", "projector power off failed")
		elif st == "KEY_R":
			#print pr.to_string()
			pr.display_file(blank=True)
			try:
				tc.send_command("mute")
			except Exception:
				lg.log_event("main.py", "projector mute failed")
		elif st == "KEY_ENTER" and pr.input_buffer != "":
			tmp_num = pr.input_buffer.lstrip("0")
			num = 0
			if len(tmp_num) == 0:
				num = 0	
			else:
				num = int(tmp_num)
			pr.input_buffer = ""
			print "ENTER: %d" % (num)
			idx = pr.find_file_index(num)
			if idx < 0:
				continue
			pr.current_file_index = idx
			pr.mem_list.append(idx)
			pr.display_file()
		elif st == "KEY_DELETE":
			pr.input_buffer = ""
		elif st == "KEY_UP":
			pr.next_file()
			pr.display_file()
		elif st == "KEY_DOWN":
			pr.prev_file()
			pr.display_file()
		elif st == "KEY_VOLUMEUP":
			pr.mem_list.increment_index()
			pr.set_cfi(pr.mem_list.get_file_index())
			pr.display_file()
		elif st == "KEY_VOLUMEDOWN":
			pr.mem_list.decrement_index()
			pr.set_cfi(pr.mem_list.get_file_index())
			pr.display_file()

