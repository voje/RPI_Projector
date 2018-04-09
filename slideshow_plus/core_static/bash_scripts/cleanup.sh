#!/bin/bash

export DISPLAY=:0

wmctrl -c Xpdf
wmctrl -c Geeqie
wmctrl -c capture_parent.sh
wmctrl -c capture.sh
