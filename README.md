### xPdf
For display, stick with this gem: [xpdf](https://www.xpdfreader.com/download.html). 
It has a server function (-remote my_server), so you don't have to kill the program for each image.  
Version 3.04 has the -remote function. 

### System dependencies:
imgmagick
xpdf (version with -remote function (3.4 has it))

### Logging
I'm using logrotate. Add a configuration file with the correct path:
```
/home/<username>/git/RPI_Projector/slideshow_plus/log/*.log {
    rotate 5
    missingok
    notifempty
    sharedscripts
    size 500k
    copytruncate
}
```
Logrotate will save up to 5 files with max size 20K.

### Settings:
* media_root_dir (/run/media/ on manjaro),
* files_dir_basename (the program looks for this folder in 
media_root_dir/<username>/, 


## Useful linux commands
```bash
# Network manager connect through terminal:
$ nmcli device wifi
$ nmcli device wifi connect

# One-liner for discovering network devices (takes a few minutes):
$ sudo nmap -sn 192.168.1.1/24 | grep -E -o -e '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | while read -r line; do echo ""; echo "##################################################"; echo "processing: $line"; nmap -A -T4 $line; done
```


## Fresh install, Raspberry 3

* Download raspbian, unzip, dd onto 16gb sd card.
* Mount the card, you should see two partitions: /boot and /rootfs.
* In `/boot`:
* Add a file named `ssh`, to enable ssh. This file gets deleted after first boot.
* Edit `config.txt`: `hdmi_force_hotplug=1`.
* In `/rootfs`:
* Edit `/etc/lightdm/lightdm.conf`: under `[Seat:\*]` edit `xserver-command=X -nocursor -s 0 -dpms`.
* Unmount card, insert it into rpi. Connect rpi to a router via ethernet. Plug in the power cable.
* Fire up a terminal, find rpi's IP.
* Use the one-liner for nmap (see this manual).
* `$sudo ssh pi@<ip>`, add key to known hosts. Default password is "raspberry".
* First time logged in, enable ssh. `$sudo systemctl enable ssh`.
* systemd, running indefinitely (tutorial)[https://bloggerbrothers.com/2016/12/20/raspberry-pi-run-on-boot-and-run-forever-systemdsystemctl/].
* `$sudo apt-get update && apt-get upgrade`.
* TODO: Install vim, git, usbmount (check if you have /etc/usbmount/) and xpdf (version 3.4 or lower).










