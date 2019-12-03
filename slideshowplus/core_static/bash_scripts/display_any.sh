#!/bin/bash

# Depends
# xpdf, geeqie, wmctrl

# Display either pdf with xpdf or try displaying other format with geeqie.

# Wait for the visual program to load the image, before
# toggling it in front of the screen.

export DISPLAY=:0
slp=0.3
filename="$1"

echo $filename

xpdf -fullscreen -remote my_xpdf "$filename" > /dev/null 2>&1 &
sleep $slp
wmctrl -a Xpdf  # bring the window forward
