# Main thread.

from flask import Flask, render_template, jsonify, request
from slideshow_plus.core import Core
import logging

log = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

core = None
buff = ""


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/remote_old")
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
        if core.file_by_number(buff):
            core.display()
        buff = ""
    else:
        buff = ""
        if key == "KEY_DELETE":
            core.del_hist_file()
        elif key == "KEY_UP":
            core.next_file()
            core.display()
        elif key == "KEY_DOWN":
            core.prev_file()
            core.display()
        elif key == "KEY_VOLUMEUP":
            core.next_hist_file()
            core.display(add_to_history=False)
        elif key == "KEY_VOLUMEDOWN":
            core.prev_hist_file()
            core.display(add_to_history=False)
        elif key == "KEY_O":
            pass
        elif key == "KEY_P":
            pass
        elif key == "KEY_R":
            pass
        else:
            success = False
    ret = jsonify({
        "success": success,
        "current_file": core.files[core.current_idx],
    })
    return ret


if __name__ == "__main__":
    # logging.basicconfig(filename="debugging.log", level=logging.debug)
    logging.basicConfig(level=logging.DEBUG)
    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi",
        default_files_dir="/home/kristjan/Pictures/mock_usb/diapozitivi1"
    )
    core.find_usb_files()

    if app.debug:
        app.run(port=5001)
    else:
        app.run("0.0.0.0")
