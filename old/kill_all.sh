#!/bin/bash

proc_names=( capture_parent.sh capture.sh autostart.sh main.py xpdf )

for proc_name in "${proc_names[@]}"; do
	if [[ $(ps -eF | grep $proc_name | wc -l) -le 1 ]]; then
		echo "${proc_name} not running."
		continue	
	fi
	proc_id=$(ps -eF | grep $proc_name | head -n 1 | tr -s ' ' | cut -d ' ' -f 2)
	kill ${proc_id}
	echo "${proc_id} killed."
done
