## xPdf
For display, stick with this gem: [xpdf](https://www.xpdfreader.com/download.html). 
It has a server function (-remote my_server), so you don't have to kill the program for each image.  
Version 3.04 has the -remote function. 

## System dependencies:
imgmagick
xpdf (version with -remote function (3.4 has it))

## Logging
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

## Settings:
* media_root_dir (/run/media/ on manjaro),
* files_dir_basename (the program looks for this folder in 
media_root_dir/<username>/, 