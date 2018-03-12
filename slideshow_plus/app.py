# Main thread.

from flask import Flask
import Core

app = Flask(__name__)
app.debug = True

core = None

if __name__ == "__main__":
    global core
    core = core.Core()

    if app.debug:
        app.run()
    else:
        app.run("0.0.0.0")
