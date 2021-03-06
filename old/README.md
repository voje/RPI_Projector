# Setting up raspberry pi from scratch #
I'll try to include as many details as I can for future reference. 

## Dictionary ##
|name|abbreviation
|---|---
|rpi|Raspberry pi
|msd|Micro SD card
|lirc|Linux infrared remote control

## Installing Raspbian ##
Requirements:
* rpi 
* computer with linux + sd card reader slot P
* msd >= 8GB  

Raspbian is a Debian based OS that runs on rpi. Download an `.img` from their official site.  
Insert msd into your linux maxhine and type:  
`$ lsblk -f`  
Find your msd device. (Something like `mmcblk0`.) Unmount it.  
Copy the raspbian image onto msd:  
`$ sudo dd if=PATH_TO_.IMG_FILE of=/dev/NAME_OF_MSD_DEVICE* bs=1M status=progress && sync`  

*NAME_OF_MSD_DEVICE vs name of a partition:  
device: '/dev/sda', partition: '/dev/sda1'.

After it's done, mount msd again. Find `/boot/config.txt` and edit some display settings:  
```bash
# If you turn on HDMI device after starting the rpi, 
# the display might not work. Fix with:  
hdmi_force_hotplug=1

# We'll be using lirc (infrared receiver).
dtoverlay=lirc-rpi,gpio_in_pin=18

# In case you need to rotate display (projection).
display_rotate=3
```

## Running root from external data storage
It's possible to move root(/) from msd to an external storage. Preferably usb-connected hard drive or perhaps a USB.  
I haven't been able to boot it from USB. (TODO)
General steps: 
* Prepare USB: GPT with one or more ext4 partitions.  
* Copy `/` from msd to USB.  Find USB/root partition UUID: `lsblk -f'. We'll call it NEW_UUID. OLD_UUID will be msd/root UUID. 
* Change settings in:
    * msd/boot/cmdline.txt:
        replace root=OLD_UUID with NEW_UUID.  
    * USB/root/etc/fstab: change root UUID from OLD_UUID to NEW_UUID.  

Plug the USB and msd into rpi and plug in the calbe. ***In theory***, you should boot into a filesystem running on the USB. 

## Set up ssh and connectivity ##
To set up ssh, use the GUI. From desktop select preferences>rpi settings (or something). Find a menu with a bunch of checkboxes. Check SSH.  
While on desktop, you should also disable USB popup menu. Uncheck:
`file manager > Edit > Preferences > Volume Management > Open mounted...inserted`.  
You also might want to change the account password. Default account is `pi` with password `raspberry`.  Change password with `$ passwd pi`.  

Next up, set up a static IP address. You need to create a new network interface. 
Create a file in `/etc/network/interfaces.d/`.  
My example: `/etc/network/interfaces.d/eth_static` with a static IP: 192.168.1.142:
```bash
# Static ethernet
auto eth0
iface eth0 inet static
address 192.168.1.142
netmask 255.255.255.0
network 192.168.1.0
gateway 192.168.1.1
dns-nameservers 8.8.8.8
```

Reboot your rpi. You should be able to connect remotely now.  
`$ ssh pi@192.168.1.142`

## Disable screen sleep ##
While using the desktop, install `xscreensaver` and disable it. 

## Disable mouse cursor
Edit file: `/etc/lightdm/lightdm.conf`. Look for `[Seat:*]` and insert:  
```
xserver-command=X -nocursor
```

## Setting up lirc ##  
First, you need to set up the hardware, i.e., connect the IR receiver to the correct pins. We're using 18 as input. Some details in the (slo) instruction in `/navodila/`. For english, google it.  
```bash
$ sudo apt-get install lirc git
```
In file `/etc/modules`, add lines (we're using pin 18 for input):
```bash
lirc_dev
lirc_rpi gpio_in_pin=18
```
Clone this repo. The path is important: `/home/pi/git/RPI_Projector/`.  
I've had some trouble getting lirc to work out of the box. This is the setps we can take to get it going. First, copy the contents of `repo/lirc` into `/etc/lirc/`. Important files are: `hardware.conf` (the repo version should work) and `lircd.conf`. You should copy the remote controller configuration into `lircd.conf`:  
```bash
$ cp /etc/lirc/remote_configs/PHILIPS_1.conf /etc/lirc/lircd.conf
```
Reload lirc and test the remote controller:  
```bash
$ sudo service lirc reload
# Testing: Press a few keys. You should see a stream of pulse,space inputs.
$ mode2 -d /dev/lirc0
# We're getting signals. Now let's test whether lircd maps the signals onto the right commands.
$ sudo irw
```
To enable sending received commands forward, enable irexec service. Copy `lircrc` into irexec configuration file. Check location with `sudo service irexec status`. In my case, it was `/etc/lirc/irexec.lircrc/`.
```bash
$ sudo service lircd enable
$ sudo service irexec enable
```

## Setting up keyboard input ##
Lirc is unreliable. I added optional usage of a USB keyboard.  
It's a bit of a hack but I'm capturing all keyboard input in a focused terminal window running a custom script `./bluetooth/capture.sh` that's mapping keyboard keys onto commands for the projection (like KEY_UP). The script is sending the commands to `ir.fifo` from where it's the same as with lirc commands.  
The script `./autostart.sh` should be ran when the desktop is finished loading. I've added it as the last line in file: `/home/pi/.config/lxsession/LXDE-pi`. The script runs the main projection script, waits for Xpdf to start a full screen slide and then starts the terminal window with `capture.sh`. It also resizes the window and keeps it focused.  

## Xpdf setup ##
There seemed to be a bug with Xpdf includes. You can comment out a line in `/etc/xpdf/xpdfrc` to avoid it.

## Run presentation script at startup ##
In `~/.bashrc`, add a line at the bottom of the file: 
```bash
/home/pi/git/RPI_Projector/autostart.sh
```


## TODO ##
* fix usb reader (folder pi/media not found)


