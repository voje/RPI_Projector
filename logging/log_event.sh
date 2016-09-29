#!/bin/bash

log_file=/home/pi/git/RPI_Projector/logging/main.log

my_time="$(date +%D,%T)"

output="[$my_time] ($1) $2"

echo "$output" | tee -a "$log_file"
