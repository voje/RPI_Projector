#!/bin/bash
#this script allows us to save pipe path in a variable

pipe="/home/pi/git/RPI_Projector/python_script/ir.fifo"

echo "$1" >"$pipe"
