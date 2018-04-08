#!/bin/bash
# Script that starts the whole application.

# Parse arguments
args=""
while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
    --no_display)
        args="$args $key"
        shift
        ;;
    --no_usb_wait)
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

# Run the flask webserver.
web_server_path="${project_dir}/slideshow_plus/flask_app/slideshow_app.py"
python3 "$web_server_path" "$args"
