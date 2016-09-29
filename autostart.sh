#!/bin/bash
python /home/pi/git/RPI_Projector/python_script/main.py 2>&1 | tee -a /home/pi/git/RPI_Projector/logging/main_err.log
