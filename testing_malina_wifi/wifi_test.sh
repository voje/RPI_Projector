#!/bin/bash

while true; do

# Check if wifi is up.
isup=$(nmcli dev wifi | grep -c malina)
echo "[$(date)] wifi malina is up: ${isup}"

# Write to file.
# todo

# reboot rpi
$(./ssh_shutdown.expect)

# Wait
sleep 30

done
