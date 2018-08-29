#!/usr/bin/python3
# Main thread.

from flask import Flask, render_template, jsonify, request
from slideshow_plus.core import Core
from os.path import dirname, join
import logging
import re
from time import sleep
import sys
from flask_cors import CORS

args = []
for arg in sys.argv:
    args.extend(arg.split())

log = logging.getLogger(__name__)
LOGFILE = join(dirname(__file__), "../log/main.log")
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:8080",
    "http://localhost:5001",
    "http://127.0.0.1:5001",
    "http://192.168.2.1:5001"
])
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
def remote():
    return render_template("remote.html")


@app.route("/remote-old")
def remote_old():
    return render_template("remote_old.html")


@app.route("/remote-stl")
def remote_stl():
    return render_template("remote_stl.html")


@app.route("/remote-vue")
def remote_vue():
    return render_template("remote_vue.html")


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
            core.display(add_to_history=False)
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
                core.set_blank(blank_on=False)
            core.projector.on()
            core.display(add_to_history=False)
        elif key == "KEY_P":
            core.projector.off()
        elif key == "KEY_R":
            core.set_blank(blank_on=True)
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


# functions used by vue_remote
def create_response ():
    response = {
        "displayed_number": core.get_current_file().get("number"),
        "sleep": core.blank,  # bool
        "on": (core.projector.state == "on"),  # bool
        "msg": "",
    }
    return response


@app.route("/get-files")
def get_files():
    files = [{"filename": x["filename"], "number": x["number"]} for x in core.files]
    response = create_response()
    response["files_list"] = files
    return jsonify(response)


@app.route("/display-file")
def display_file():
    number = request.args.get("number")
    response = create_response()
    if number is None:
        response["msg"] = "Missing arg: number."
    elif (core.file_by_number(number)):
        core.display()
        response["displayed_number"] = core.get_current_file().get("number")
    else:
        response["msg"] = "File not found."
    return jsonify(response)


@app.route("/change-state", methods=["POST"])
def change_state():
    input_json = request.json
    core.set_blank(blank_on=input_json["sleep"])
    core.projector.on() if input_json["on"] else core.projector.off()
    core.display(add_to_history=False)
    return jsonify(create_response())

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
