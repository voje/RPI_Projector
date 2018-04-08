#!/bin/bash

#This is a test script

wname="capture.sh"

while [[ -z $(wmctrl -l | grep "$wname") ]]; do
	:	
done

echo "LOOK, a wild $wname appeared!"
