#!/bin/bash
# Run capture.sh and keep it focused.

wname="capture.sh"

# Run the window
x-terminal-emulator --command=/home/pi/git/RPI_Projector/bluetooth/capture.sh --title=$wname &

while [[ -z $(wmctrl -l | grep "$wname") ]]; do
	sleep 0.5
done
echo "LOOK, a wild $wname appeared!"

# Resize and move (top-left, smallest possible)
wmctrl -r "$wname" -e "0,490,0,1,1"

# Keep in foreground
while true; do
	wmctrl -a "$wname"
	sleep 0.5
done



