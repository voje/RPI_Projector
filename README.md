# Setting up raspberry pi from scratch #
I'll try to include as many details as I can for future reference. 

## Dictionary ##
|name|abbreviation
|---|---
|rpi|Raspberry pi
|msd|Micro SD card

## Installing Raspbian ##
Requirements:
* rpi 
* computer with linux + sd card reader slot 
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
dtoverlay=lirc-rpi
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
You might want to change the password. Default account is `pi` with password `raspberry`.  Change password with `$ passwd pi`.  

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



