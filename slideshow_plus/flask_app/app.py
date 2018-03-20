# Main thread.

from flask import Flask, render_template
from slideshow_plus.core import Core

app = Flask(__name__)
app.debug = True

core = None


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi"
    )
    core.find_usb_files()

    if app.debug:
        app.run()
    else:
        app.run("0.0.0.0")
