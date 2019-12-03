#!/bin/bash
# Script that starts the whole application.

export DISPLAY=:0

project_dir="/home/${USER}/git/RPI_Projector"

capture_parent_pid=""

function fn_cleanup() {
	echo "Clenup after kill."
	bash "${project_dir}/slideshowplus/core_static/bash_scripts/cleanup.sh"	
	if [ $capture_parent_pid ]; then
		kill $capture_parent_pid
	fi
}
trap fn_cleanup INT

# Parse arguments
args=""

capture_keyboard="true"

while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
    -h | --help)
        echo "args:
        --kill
        --no_display
        --no_usb_wait
        --no_keyboard"
        exit
        ;;
    --kill)
	    fn_cleanup
	    exit
        ;;
    --no_display)
        args="$args $key"
        shift
        ;;
    --no_usb_wait)
        args="$args $key"
        shift
        ;;
    --no_keyboard)
        capture_keyboard="false"
        shift
        ;;
    *)
        echo "Unknown command."
	exit
        ;;
    esac
done

# If we're capturing keyboard, run the capture_parent.sh
if [[ $capture_keyboard == "true" ]]; then
    bash "${project_dir}/bluetooth/capture_parent.sh" &
	capture_parent_pid=$!
fi

# Run the flask webserver.
web_server_path="${project_dir}/slideshowplus/flask_app/slideshow_app.py"
python3 "$web_server_path" "$args"


