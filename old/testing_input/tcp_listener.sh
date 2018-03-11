#!/bin/bash
while true
do 
	echo "TESTPROJECTOR_RESPONSE" | netcat -l 127.0.0.1 4352
	sleep 2s
done
