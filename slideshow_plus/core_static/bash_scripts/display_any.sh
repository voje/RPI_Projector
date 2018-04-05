#!/bin/bash

# Depends
# xpdf, geeqie, wmctrl

# Display either pdf with xpdf or try displaying other format with geeqie.

# Wait for the visual program to load the image, before
# toggling it in front of the screen.
slp=0.3

filename=$1

if [ $(head -c 4 "${filename}") = "%PDF" ]; then
    # echo "using xpdf"
    xpdf -fullscreen -remote my_xpdf "$filename" &
    sleep $slp
    wmctrl -a Xpdf  # bring the window forward
else
    # echo "using geeqie"
    geeqie -r -fs "$filename" &
    sleep $slp

    # Just in case, wait for geeqie to load the fullscreen window.
    wmctrl -l | grep "Full screen"
    if [ $(wmctrl -l | grep "Full screen" | wc -l) -lt 1 ]; then
        ttime=1000
        while [ $(wmctrl -l | grep "Full screen" | wc -l) -lt 1 ]; do
            # echo "waiting for geeqie fullscreen: [$ttime]"
            wmctrl -l | grep "Full screen"
            (( ttime-- ))
            if (( ttime <= 0 )); then
                echo "waiting for geeqie fullscreen: timed out!"
                exit 1
            fi
        done
        sleep $slp
    fi

    wmctrl -a Full
fi
