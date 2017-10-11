#!/bin/bash

# Set right screen
export DISPLAY=:0

# Start main.py
/home/pi/git/RPI_Projector/python_script/main.py 2>> /home/pi/git/RPI_Projector/logging/main_err.log &

# Wait for Xpdf
wname="Xpdf:"
while [[ -z $(wmctrl -l | grep "$wname") ]]; do
	echo "Waiting for $wname."
	sleep 0.5
done
echo "LOOK, a wild $wname appeared!"

# Start capturing bluetooth keyboard in a focused terminal
/home/pi/git/RPI_Projector/bluetooth/capture_parent.sh
