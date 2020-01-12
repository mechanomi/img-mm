import mimetypes
import os
import pathlib
import random
import sys
import threading
import webbrowser
import urllib

from flask import request

from urllib.parse import unquote, quote

import flask
import trueskill
import xattr

from pprint import pprint, pformat

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

filenames = sys.argv[1:]
eligible_filenames = []
for filename in filenames:
    filename_ext = pathlib.Path(filename).suffix.lower()
    if filename_ext not in SUPPORTED_EXTS:
        continue
    eligible_filenames.append(filename)

def get_file(filename):
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
    mu = float(mu.decode("UTF8"))
    sigma = float(sigma.decode("UTF8"))
    rating = trueskill.Rating(mu=mu, sigma=sigma)
    return {
        "filename": quote(filename),
        "mtime": os.path.getmtime(filename),
        "previous_rating": previous_rating,
        "rating": rating
    }

def update_file(filename, mu, sigma):
    file_xattr = xattr.xattr(unquote(filename))
    file_xattr.set(MU_XATTR, str(mu).encode('UTF8'))
    file_xattr.set(SIGMA_XATTR, str(sigma).encode('UTF8'))

def update_rankings(win, lose):
    win_file = get_file(win)
    lose_file = get_file(lose)
    win_rating, lose_rating = \
        trueskill.rate_1vs1(win_file["rating"], lose_file["rating"])
    print("before")
    print(win_file["filename"] + " - " + pformat(win_file["rating"]))
    print(lose_file["filename"] + " - " + pformat(lose_file["rating"]))
    print("after")
    print(win_file["filename"] + " - " + pformat(win_rating))
    print(lose_file["filename"] + " - " + pformat(lose_rating))
    update_file(win_file["filename"], win_rating.mu, win_rating.sigma)
    update_file(lose_file["filename"], lose_rating.mu, lose_rating.sigma)

@app.route('/img')
def img():
    filename = request.args.get('filename')
    print("display: " + filename)
    img_file = open(filename, "rb")
    mimetype = mimetypes.guess_type(filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)

@app.route('/')
def index():
    win = request.args.get('win')
    lose = request.args.get('lose')
    if win is not None and lose is not None:
        update_rankings(unquote(win), unquote(lose))
    match_filenames = random.sample(eligible_filenames, 2)
    context = {
        "files": [
            get_file(match_filenames[0]),
            get_file(match_filenames[1])
        ]
    }
    return flask.render_template(TEMPLATE, **context)

if __name__ == '__main__':
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()

