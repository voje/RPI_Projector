#!/bin/bash
# Script that starts the whole application.

# Parse arguments
args=""
capture_keyboard=false
while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
    --help)
        echo "args:
        --no_display
        --no_usb_wait
        --capture_keyboard"
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

# Helps if we're running it from ssh.
export DISPLAY=:0

project_dir=$(pwd $(dirname "$0"))

# If we're capturing keyboard, run the capture_parent.sh
if $capture_keyboard; then
    bash "${project_dir}/bluetooth/capture_parent.sh"
fi

# Run the flask webserver.
web_server_path="${project_dir}/slideshow_plus/flask_app/slideshow_app.py"
python3 "$web_server_path" "$args"


