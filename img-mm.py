import os
import sys
import webbrowser
import threading

import flask


app = flask.Flask(__name__)

APP_URL = 'http://127.0.0.1:5000/'
TEMPLATE = "img-mm.tpl"

@app.route('/')
def hello_world():
    context = {"argv": sys.argv}
    return flask.render_template(TEMPLATE, context=context)

if __name__ == '__main__':
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()

