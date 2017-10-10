#!/bin/bash

# Set right screen
export DISPLAY=:0

# Start main.py
/home/pi/git/RPI_Projector/python_script/main.py 2>> /home/pi/git/RPI_Projector/logging/main_err.log &

# Start keyboard listener
sleep	10 #todo.. wait for xpdf

# Start capturing bluetooth keyboard in a focused terminal
/home/pi/git/RPI_Projector/bluetooth/capture_parent.sh &
