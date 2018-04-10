#!/usr/bin/python3
# Main thread.

from flask import Flask, render_template, jsonify, request
from slideshow_plus.core import Core
from os.path import dirname, join
import logging
import re
from time import sleep
import sys

args = []
for arg in sys.argv:
    args.extend(arg.split())

log = logging.getLogger(__name__)
LOGFILE = join(dirname(__file__), "../log/main.log")
app = Flask(__name__)
core = None
buff = ""
re_zeros = re.compile(r'000[1-9]+')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/log")
def log():
    lines = []
    with open(LOGFILE, "r") as file:
        for line in file:
            lines.insert(0, line)
    return "<br><br>".join(lines)


@app.route("/remote")
def remote_old():
    return render_template("remote_old.html")


@app.route("/command")
def command():
    global buff
    key = request.args.get("key")
    success = True
    if key.isdigit():
        buff += key
    elif key == "KEY_ENTER":
        if re_zeros.findall(buff):
            core.special_command(buff)
        elif core.file_by_number(buff):
            core.display()
        buff = ""
    else:
        buff = ""
        if key == "KEY_DELETE":
            core.del_hist_file()
        elif key == "KEY_UP":
            core.next_file()
            core.display(add_to_history=False)
        elif key == "KEY_DOWN":
            core.prev_file()
            core.display(add_to_history=False)
        elif key == "KEY_VOLUMEUP":
            core.next_hist_file()
            core.display(add_to_history=False)
        elif key == "KEY_VOLUMEDOWN":
            core.prev_hist_file()
            core.display(add_to_history=False)
        elif key == "KEY_O":
            if core.blank:
                core.toggle_blank("off")
            core.projector.on()
        elif key == "KEY_P":
            core.projector.off()
        elif key == "KEY_R":
            core.toggle_blank("on")
        else:
            success = False
    current_file = (
        None if core.current_idx < 0 else core.files[core.current_idx]
    )
    ret_dict = {
        "success": success,
        "current_file": current_file,
        "blank": core.blank,
        "projector_state": core.projector.state
    }
    ret = jsonify(ret_dict)
    return ret


if __name__ == "__main__":
    # Most of the settings in here. TODO: config file.
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
    # logging.basicConfig(level=logging.DEBUG)
    app.debug = False

    if "--no_usb_wait" not in args:
        sleep(20)

    core = Core(
        media_root_dir="/media",
        files_dir_basename="diapozitivi",
        no_display="--no_display" in args
    )

    if app.debug:
        app.run(port=5001)
    else:
        app.run("0.0.0.0", port=5001)
