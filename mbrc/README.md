# mbrc #
Mobile Browser-based Remote Control. Written in pure *html,css,javascript* for compatibility with older devices.  

## Running the whole thing: ##
From root dir, run: `node server/server.js`.  
Access the public client from port 3345.  

## Problem I'm solving: ##
I need to control a RPI over 40m of obscured terrain. RPI needs to accept numeric input and 5 function keys.  

## Solution: ##
Plug RPI onto a wireless router (also helpful for debugging the RPI).  
Run a server on RPI, that listens to signals from a browser based keyboard.  
The keyboard can be accessed through any device with a browser, connected to the local wireless network.  
I'm going to recycle an old android phone and use it as a remote control. *Android 2.3.6*

### Why not an Android app? ###
For simplicity. I'll use an old Samsung as a remote controller but other people should be able to access the system with their own devices. Since it's a simple app, installing it on every device seems like overkill. There may also be compatibility issues, if someone shows up with an iPhone.  

## Notes: ##

* Compatibility might be a problem. The old Samsung I'm using is running *Android 2.3.6*.  
* jQuery supported on: Stock browser on Android 4.0+ ...sigh. Whelp, I'm stuck with pure javascript.  
* Twitter Bootstrap supported on: Android v5.0+ ...yeah.  
