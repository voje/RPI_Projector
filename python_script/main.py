#!/usr/bin/python

import os
import presenter
import tcp_client
import time
import logger_wrapper
import thread

if __name__ == "__main__":
	lg = logger_wrapper.LoggerWrapper(l_on=True)
	lg.log_event("main.py", "##### Starting powerpoint script. #####")
	pr = presenter.Presenter(20, logger=lg)
	tc = tcp_client.TcpClient(logger=lg)

	print "Client ready."

	#initially display file 0
	time.sleep(20);     #todo
	pr.ul.find_usbs()
	if pr.ul.new_usb():
		#print "USB initially present."
		pr.ul.get_dir_path()
		lg.log_event( "main.py", "USB initially present: %s" % (pr.ul.dir_path) )
		pr.get_files_list(pr.ul.dir_path)
	pr.display_file()

	#time_start = time.time()

        #Open fifo
	#FIFO = os.open(pr.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
	FIFO = open(pr.fifo_path, 'r')

	while True:
		#time.sleep(0.3)

		#debugging this loop (not necessary, we'll be waiting for events in the fifo loop)
                """
		time_diff = time.time() - time_start
		time_start = time.time()
		if time_diff > 10:
			lg.log_event( "main.py", "MAIN_LOOP_ERROR: long cycle in main loop" )
                """

		#check if new USB was inserted
		pr.ul.find_usbs()
		if pr.ul.new_usb():
			pr.ul.get_dir_path()
			lg.log_event( "main.py", "USB change detected: %s" % (pr.ul.dir_path) )
			pr.get_files_list(pr.ul.dir_path)
			#display first file from storage
			pr.display_file()

		#check fifo for new input from ir remote
		read_done = False
		st = "" 
		while not read_done:
			try:
				#st = os.read(FIFO, 200)
                                st = FIFO.readline()
                                if st != "":
                                    read_done = True
				#print "FIFO: %s" % (st)
			except:
				pass

                # Possible error handling
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
				#thread.start_new_thread(tc.send_command("on"), ())
				lg.log_event("main.py", "projector power on")
				tc.send_command("on")
			except Exception as e:
				lg.log_event("main.py", "power on exception: %s" % (e))
		elif st == "KEY_P":
			try:
				#thread.start_new_thread(tc.send_command("off"), ())
				lg.log_event("main.py", "projector power off")
				tc.send_command("off")
			except Exception as e:
				lg.log_event("main.py", "power off exception: %s" % (e))
		elif st == "KEY_R":
			#print pr.to_string()
			lg.log_event("main.py", "projector blank file")
			pr.display_file(blank=True)
		elif st == "KEY_ENTER" and pr.input_buffer != "":
			tmp_num = pr.input_buffer.lstrip("0")
			num = 0
			if len(tmp_num) == 0:
				num = 0	
			else:
				num = int(tmp_num)
			pr.input_buffer = ""
			#print "ENTER: %d" % (num)
			idx = pr.find_file_index(num)
			if idx < 0:
				continue
			pr.current_file_index = idx
			pr.mem_list.append(idx)
			pr.display_file()
		elif st == "KEY_DELETE":
			pr.input_buffer = ""
                        pr.mem_list.pop()
                        pr.set_cfi(pr.mem_list.get_file_index())
                        pr.display_file()
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
