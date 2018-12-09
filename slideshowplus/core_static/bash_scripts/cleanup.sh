#!/bin/bash

export DISPLAY=:0

wmctrl -c Xpdf
wmctrl -c Geeqie
wmctrl -c capture_parent.sh
wmctrl -c capture.sh

# just to be safe
pkill -u pi Xpdf
pkill -u pi Geeqie
pkill -u pi capture_parent.sh
pkill -u pi capture.sh
pkill -u pi autostart.sh
pkill -u pi python3
