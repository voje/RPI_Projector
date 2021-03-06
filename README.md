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
/home/<username>/git/RPI_Projector/slideshowplus/log/*.log {
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
$ sudo nmap -sn 192.168.2.1/24 | grep -E -o -e '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | while read -r line; do echo ""; echo "##################################################"; echo "processing: $line"; nmap -A -T4 $line; done
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
* `$sudo apt-get update && apt-get upgrade`.
* Install some programs: `$sudo apt-get install vim git wmctrl geeqie imagemagick paps ghostscript usbmount xpdf`
* xpdf should be version 3.4 or lower (one with a -remote option)
* To disable removable media popup, edit `~/.config/pcmanfm/LXDE-pi/pcmanfm.conf`: `autorun=0`
* Create an access point ((tutorial)[https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md].
* Adding to the tutorial:
* If needed, unblock wireless interface: `$sudo rfkill unblock wifi`.
* In `/etc/dhcpcd.conf`, added the following:
```
interface wlan0
static ip_address=192.168.2.1/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
nohook wpa_supplicant
```
* Reboot rpi. It should show up in your wifi menu now.
* ssh onto rpi, git clone the app, run `$pip3 --user -e install .` in the folder with `.setup.py`.
* App settings:
* disable debug mode
* set port (the same one you will open, 5003 in my case)
* set media_root_dir (on manjaro it was /run/media, on raspbian it was /media)
* open the app port in iptables:  
```
$ sudo iptables -A INPUT -p tcp -m tcp --dport 5003 -j ACCEPT
$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
Also make sure iptables get reloaded on startup. 
* enable fire up autostart.sh on desktop load:
* in `./config/lxsession/<user_session>/autostart` add a line: `@/home/pi/git/RPI_Projector/autostart.sh`.
* in `autostart.sh`, change the start parameters (capture keyboard, ...)
* in `slideshow_app.py` change debug level
* to disable desktop pop-up notifications when removing USB: remove external devices manager icon (top right on desktop)


## DNS settings
To run the raspberry with a local DNS.
(blog post)[https://www.linux.com/learn/dnsmasq-easy-lan-name-services]
Check out `./system_config`.
We alse want `dnsmasq` to run at boot.
```$ sudo systemctl enable dnsmasq```

## iptables port redirection
We want to access out app (port 5001) from default 80.
(Might need to change wlan0 to something else.)
```bash
$ sudo iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
$ sudo iptables -A PREROUTING -t nat -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 5001
# save the rules to a file
$ sudo iptables-save > iptables.conf
```
We will need to restore iptables config on every boot.
Put a line in `/etc/rc.local` before `exit 0`.
```bash
# Restore firewall settings (from the access point tutorial).
iptables-restore < /home/pi/git/RPI_Projector/system_config/iptables/iptables.conf

exit 0
```

After a reboot, find a network called `malina`, type in a password `malina18`, fire up a browser and go to `pi.malina`.

## Some useful tools

* Write your own systemd service in `/etc/systemd/system/my-service.service`
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl my-service enable/start
```
* ```$ systemd-analyse plot > plot.svg```

## Migrating app dev -> production
Api address in `vue_frontend/src/main.js`.  
Loggin mode in `flask_app/slideshow_app.py`
