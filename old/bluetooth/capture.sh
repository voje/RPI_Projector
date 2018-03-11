#!/bin/bash

IFS='£' #I want to catch enter and space.
pipe="/home/pi/git/RPI_Projector/python_script/ir.fifo"

while true; do
	out=''
	read -s -d '' -n 1 key
	#read keys with more than 1 symbol
	#while read -sn 1 -t .01 y; do key="$key$y"; done
	#echo -e "$key"
	case "$key" in
	$'\E')
		read -s -d '' -n 1 -t 0.01 key2
		read -s -d '' -n 1 -t 0.01 key3
		read -s -d '' -n 1 -t 0.01 key4 #up to 4 characters
		#echo "$key $key2 $key3 $key4"
		case "$key2" in
		'')
			echo "Esc key"
			out="KEY_P"
			;;
		*)
			case "$key3" in
			'A')
			    echo "Arrow up"
			    out="KEY_UP"
			    ;;
			'B')
			    echo "Arrow down"
			    out="KEY_DOWN"
			    ;;
			'C')
			    echo "Arrow right"
			    out="KEY_VOLUMEUP"
			    ;;
			'D')
			    echo "Arrow left"
			    out="KEY_VOLUMEDOWN"
			    ;;
			esac
			;;
		esac
		;;
	[0-9])
		echo "$key"     
		out="$key"
		;;
	$'\n')
		echo "Enter key"
		out="KEY_ENTER"
		;;
	$' ')
		echo "Space key"
		out="KEY_O"
		;;
	$'+')
		echo "Plus"
		out="KEY_O"
		;;
	$'-')
		echo "Minus"
		out="KEY_P"
		;;
	$'\177')
		echo "Backspace key"
		out="KEY_DELETE"
		;;
	'`')
		echo "Quote 3"
		out="KEY_R"
		;;
	'*')
		echo "Star"
		out="KEY_R"
		;;
	*)
		printf "####%q####\n" "$key" 
		#out="unknown"
		;;
	esac
    
	# Send to fifo, log
	if [[ ! -z "$out" ]]; then
		#echo $out
		#echo ''
		echo "$out" >"$pipe"
		/home/pi/git/RPI_Projector/logging/log_event.sh "capture.sh" "$out"
	fi

done
