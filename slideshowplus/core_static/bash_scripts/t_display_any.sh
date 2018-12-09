#!/bin/bash

# prologue
geeqie -r
wmctrl -r Geeqie -e 0,-10000,-10000,0,0

directory="../diapozitivi"

for filename in $(ls "$directory"); do
    echo "displaying: $filename"
    ./display_any.sh "$directory/$filename" &
    sleep 3
done

sleep 7

# epilogue
wmctrl -c Xpdf
wmctrl -c Geeqie