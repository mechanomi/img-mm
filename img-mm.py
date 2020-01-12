import os
import sys
import webbrowser
import threading

import flask


app = flask.Flask(__name__)

APP_URL = 'http://127.0.0.1:5000/'
TEMPLATE = "img-mm.tpl"

@app.route('/')
def main():
    filenames = sys.argv[1:]
    files = []
    for filename in filenames:
        files.append({
            "filename": filename,
            "mtime": os.path.getmtime(filename)
        })
    context = {
        "files": files
    }
    return flask.render_template(TEMPLATE, **context)

if __name__ == '__main__':
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()

