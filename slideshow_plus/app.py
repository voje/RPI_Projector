# Main thread.

from flask import Flask

app = Flask(__name__)
app.debug = True

if __name__ == "__main__":
    if app.debug:
        app.run()
    else:
        app.run("0.0.0.0")
