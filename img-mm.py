import os
import sys
import webbrowser
import threading

from pprint import pformat

from flask import Flask
app = Flask(__name__)


APP_URL = 'http://127.0.0.1:5000/'

@app.route('/')
def hello_world():
    return pformat(sys.argv)

if __name__ == '__main__':
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()
