#!/bin/bash
#random input from remote, try to break the script

declare -a commands1=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'KEY_ENTER' 'KEY_DELETE' 'KEY_UP' 'KEY_DOWN' 'KEY_VOLUMEUP' 'KEY_VOLUMEDOWN' 'KEY_O' 'KEY_P' 'KEY_R' )
declare -a commands2=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'KEY_ENTER' 'KEY_DELETE' 'KEY_UP' 'KEY_DOWN' 'KEY_VOLUMEUP' 'KEY_VOLUMEDOWN' )
declare -a commands3=( 'KEY_O' 'KEY_P' 'KEY_R' )

declare -a sleep_times=( '0.1' '0.2' '0.3' '0.5' '0.6' '0.7' '0.8' '0.9' '1.0' '1.4' '2.0' )

commands=(${commands1[@]})

n_commands=${#commands[@]}
n_sleep_times=${#sleep_times[@]}

pipe="/home/pi/git/RPI_Projector/python_script/ir.fifo"

#for i in $(seq 1 10); do
while true; do
	slp_idx=$(( ($RANDOM % $n_sleep_times) ))
	slp=${sleep_times[$slp_idx]}
	#slp=0.1
	#echo $slp
	cmd_idx=$(( ($RANDOM % $n_commands) ))
	cmd=${commands[$cmd_idx]}
	#echo $cmd
	#sleep $slp
	#echo -e "('$slp's)\t\t$cmd" >> random_input.log
	echo "$cmd" >"$pipe"
done
