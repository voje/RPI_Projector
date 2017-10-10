#!/bin/bash
# Run capture.sh and keep it focused.

wname="capture.sh"

# Run the window
x-terminal-emulator --command="home/pi/git/RPI_Projector/capture.sh" --title="$wname"

# Resize and move (top-left, smallest possible)
wmctrl -r "$wname" -e "0,0,0,3,6"

# Keep in foreground
while true; do
	wmctrl -a "$wname"
done
