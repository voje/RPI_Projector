#!/bin/bash
#this script allows us to save pipe path in a variable

pipe="/home/pi/git/RPI_Projector/python_script/ir.fifo"

#running:
echo "$1" >"$pipe"
/home/pi/git/RPI_Projector/logging/log_event.sh "lirc" "$1"

#testing:
#echo "$1" | tee -a "$pipe" "/home/pi/git/RPI_Projector/testing.log"
