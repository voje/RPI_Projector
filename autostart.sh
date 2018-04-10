#!/bin/bash
# Script that starts the whole application.

export DISPLAY=:0

project_dir="/home/${USER}/git/RPI_Projector"

capture_parent_pid=""

function fn_cleanup() {
	echo "Clenup after kill."
	bash "${project_dir}/slideshow_plus/core_static/bash_scripts/cleanup.sh"	
	if [ $cleanup_pid ]; then
		kill $capture_parent_pid
	fi
}
trap fn_cleanup INT

# Parse arguments
args=""

capture_keyboard=false

while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
    --help)
        echo "args:
        --kill
        --no_display
        --no_usb_wait
        --capture_keyboard"
        exit
        ;;
    --kill)
        kill_all=true 
        shift
        ;;
    --no_display)
        args="$args $key"
        shift
        ;;
    --no_usb_wait)
        args="$args $key"
        shift
        ;;
    --capture_keyboard)
        capture_keyboard=true
        args="$args $key"
        shift
        ;;
    *)
        shift
        ;;
    esac
done

if $kill_all; then
    fn_cleanup
fi

# Hardcoded...
capture_keyboard=false

# If we're capturing keyboard, run the capture_parent.sh
if $capture_keyboard; then
    	bash "${project_dir}/bluetooth/capture_parent.sh" &
	capture_parent_pid=$!
fi

# Run the flask webserver.
web_server_path="${project_dir}/slideshow_plus/flask_app/slideshow_app.py"
python3 "$web_server_path" "$args"


