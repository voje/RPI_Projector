# Main thread.

from flask import Flask, render_template, jsonify, request
from slideshow_plus.core import Core
import logging
import re

log = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

core = None
buff = ""
# 0001,... special commands
zeros = re.compile(r'000[1-9]+')


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
        if zeros.findall(buff):
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
                core.toggle_blank()
            core.projector.on()
        elif key == "KEY_P":
            core.projector.off()
        elif key == "KEY_R":
            core.toggle_blank()
        else:
            success = False
    ret = jsonify({
        "success": success,
        "current_file": core.files[core.current_idx],
        "blank": core.blank,
        "projector_state": core.projector.state
    })
    return ret


if __name__ == "__main__":
    # logging.basicconfig(filename="debugging.log", level=logging.debug)
    logging.basicConfig(level=logging.DEBUG)
    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi"
    )

    if app.debug:
        app.run(port=5001)
    else:
        app.run("0.0.0.0")
