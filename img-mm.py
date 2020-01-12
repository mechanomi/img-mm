import mimetypes
import os
import pathlib
import random
import sys
import threading
import webbrowser
import urllib

import flask
import trueskill
import xattr

app = flask.Flask(__name__)

APP_URL = 'http://127.0.0.1:5000/'
TEMPLATE = "img-mm.tpl"
MU_XATTR = "ts.mu"
SIGMA_XATTR = "ts.sigma"
SUPPORTED_EXTS = [
    ".bmp"
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".webp",
]

@app.route('/img')
def img():
    filename = flask.request.args.get('filename')
    img_file = open(filename, "rb")
    mimetype = mimetypes.guess_type(filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)

@app.route('/')
def index():
    filenames = sys.argv[1:]
    files = []
    for filename in filenames:
        filename_ext = pathlib.Path(filename).suffix.lower()
        if filename_ext not in SUPPORTED_EXTS:
            continue
        file_xattr = xattr.xattr(filename)
        try:
            mu = file_xattr.get(MU_XATTR)
        except OSError:
            mu = None
        try:
            sigma = file_xattr.get(SIGMA_XATTR)
        except OSError:
            sigma = None
        previous_rating = False
        if mu is not None or sigma is not None:
            previous_rating = True
        rating = trueskill.Rating(mu=mu, sigma=sigma)
        files.append({
            "filename": urllib.parse.quote(filename),
            "mtime": os.path.getmtime(filename),
            "previous_rating": previous_rating,
            "rating": rating
        })
    context = {
        "files": random.sample(files, 2)
    }
    return flask.render_template(TEMPLATE, **context)

if __name__ == '__main__':
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()

