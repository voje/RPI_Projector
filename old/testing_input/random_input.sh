#!/bin/bash
#random input from remote, try to break the script

declare -a commands1=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'KEY_ENTER' 'KEY_DELETE' 'KEY_UP' 'KEY_DOWN' 'KEY_VOLUMEUP' 'KEY_VOLUMEDOWN' 'KEY_O' 'KEY_P' 'KEY_R' )
declare -a commands2=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'KEY_ENTER' 'KEY_DELETE' 'KEY_UP' 'KEY_DOWN' 'KEY_VOLUMEUP' 'KEY_VOLUMEDOWN' )
declare -a commands3=( 'KEY_O' 'KEY_P' 'KEY_R' )
declare -a digits=( '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' )
declare -a commands4=( 'KEY_ENTER' 'KEY_DELETE' 'KEY_UP' 'KEY_DOWN' 'KEY_VOLUMEUP' 'KEY_VOLUMEDOWN' 'KEY_O' 'KEY_P' 'KEY_R' )
n_buffered_digits=0

declare -a sleep_times=( '0.1' '0.2' '0.3' '0.5' '0.6' '0.7' '0.8' '0.9' '1.0' '1.4' '2.0' )

commands=(${commands4[@]})

n_commands=${#commands[@]}
n_digits=${#digits[@]}
n_sleep_times=${#sleep_times[@]}

pipe="/home/pi/git/RPI_Projector/python_script/ir.fifo"

#for i in $(seq 1 10); do
while true; do
	echo "tutal buffered... $n_buffered_digits"
	cmd_idx=$(( ($RANDOM % $n_commands) ))
	cmd=${commands[$cmd_idx]}

	if (( ($RANDOM % 10) > 3 )); then
		if (( $n_buffered_digits < 3 )); then
			digit_idx=$(( ($RANDOM % $n_digits) ))
			digit=${digits[$digit_idx]}
			cmd=${digit}
			n_buffered_digits=$(( n_buffered_digits + 1 ))
		else
			cmd="KEY_ENTER"
		fi
	fi

	if [[ ${cmd} == "KEY_ENTER" ]]; then
		echo "reset"
		n_buffered_digits=0
	fi

	slp_idx=$(( ($RANDOM % $n_sleep_times) ))
	slp=${sleep_times[$slp_idx]}
	#slp=0.1
	sleep $slp

	#testing
	#echo $cmd
	#echo -e "('$slp's)\t\t$cmd" >> random_input.log

	#log
	$(/home/pi/git/RPI_Projector/logging/log_event.sh "random_input.sh" "$cmd")

	#to pipe
	echo "$cmd" >"$pipe"
done
