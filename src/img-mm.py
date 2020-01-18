import mimetypes
import os
import pathlib
import re
import shutil
import sys
import threading
import webbrowser

from flask import request

from urllib.parse import unquote

import flask
import trueskill
import xattr

from pprint import pprint

app = flask.Flask(__name__)

APP_URL = 'http://127.0.0.1:5000/'
RANK_MULTIPLIER = 1000
TEMPLATE = "img-mm.tpl"
MU_XATTR = "img-mm.ts.mu"
SIGMA_XATTR = "img-mm.ts.sigma"
PREV_MU_XATTR = "img-mm.ts.mu.prev"
PREV_SIGMA_XATTR = "img-mm.ts.sigma.prev"
PREV_INDEX_XATTR = "img-mm.index.prev"
PREV_FILENAME_XATTR = "img-mm.filename.prev"
SUPPORTED_EXTS = [
    ".bmp"
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".webp",
]

eligible_files = []

files_index = {}


def rank(rating):
    rank = str(
        (50 * RANK_MULTIPLIER) - round(
            (rating.mu - (3 * rating.sigma)) * RANK_MULTIPLIER
        )
    )
    return rank


def get_xattr(filename, name):
    try:
        value = xattr.getxattr(filename, name).decode("UTF8")
    except OSError:
        value = None
    return value


def set_xattr(filename, name, value):
    xattr.setxattr(filename, name, value.encode('UTF8'))


def get_file(filename):
    mu = get_xattr(filename, MU_XATTR)
    sigma = get_xattr(filename, SIGMA_XATTR)
    prev_mu = get_xattr(filename, PREV_MU_XATTR)
    prev_sigma = get_xattr(filename, PREV_SIGMA_XATTR)
    prev_index = get_xattr(filename, PREV_INDEX_XATTR)
    prev_filename = get_xattr(filename, PREV_FILENAME_XATTR)
    previous_rating = False
    if mu is not None or sigma is not None:
        previous_rating = True
        rating = trueskill.Rating(mu=float(mu), sigma=float(sigma))
    else:
        rating = trueskill.Rating()
    return {
        "filename": filename,
        "mtime": os.path.getmtime(filename),
        "previous_rating": previous_rating,
        "rating": rating,
        "prev_mu": prev_mu,
        "prev_sigma": prev_sigma,
        "prev_index": prev_index,
        "prev_filename": prev_filename,
        "rank": rank(rating)
    }


def update_file(file_dict, rating, rm=False):
    filename = file_dict["filename"]
    print("Update from %s to %s" % (file_dict["rating"].mu, rating.mu))
    # Save previous state
    set_xattr(filename, PREV_MU_XATTR, str(file_dict["rating"].mu))
    set_xattr(filename, PREV_SIGMA_XATTR, str(file_dict["rating"].sigma))
    set_xattr(filename, PREV_INDEX_XATTR, str(files_index[filename]))
    set_xattr(filename, PREV_FILENAME_XATTR, filename)
    # Update state
    set_xattr(filename, MU_XATTR, str(rating.mu))
    set_xattr(filename, SIGMA_XATTR, str(rating.sigma))
    path = pathlib.PurePath(filename)
    suffix = re.split(r'^(\d+R)\s+?', path.name)[-1]
    new_name = "%sR %s" % (rank(rating), suffix)
    if not rm:
        new_filename = str(path.parent.joinpath(new_name))
    else:
        path = pathlib.PurePath("/tmp")
        new_filename = str(path.joinpath(new_name))
    shutil.move(filename, new_filename)
    new_file = get_file(new_filename)
    for i, file in enumerate(eligible_files):
        if file["filename"] == filename:
            if not rm:
                eligible_files[i] = new_file
            else:
                del(eligible_files[i])
    return new_file


def handle_match(win, lose, rm=False):
    pprint(("handle_match", win, lose, rm))
    try:
        win_file = get_file(win)
        lose_file = get_file(lose)
    except FileNotFoundError:
        # File has gone. User might have refreshed page after file was renamed.
        # Either way, no way to recover, so take no action.
        return
    win_rating, lose_rating = \
        trueskill.rate_1vs1(win_file["rating"], lose_file["rating"])
    print("Before:")
    print("  Win:  " + rank(win_file["rating"]) + " " + win_file["filename"])
    print("  Lose: " + rank(lose_file["rating"]) + " " + lose_file["filename"])
    print("After:")
    print("  Win:  " + rank(win_rating) + " " + win_file["filename"])
    print("  Lose: " + rank(lose_rating) + " " + lose_file["filename"])
    win_file = update_file(win_file, win_rating)
    lose_file = update_file(lose_file, lose_rating, rm)
    if not rm:
        results = {"win": win_file, "lose": lose_file}
    else:
        results = {"win": win_file, "rm": lose_file}
    pprint(results)
    return results


def undo_update_file(filename, rm=False):
    # Get previous state
    prev_mu = get_xattr(filename, PREV_MU_XATTR)
    prev_sigma = get_xattr(filename, PREV_SIGMA_XATTR)
    prev_index = get_xattr(filename, PREV_INDEX_XATTR)
    prev_filename = get_xattr(filename, PREV_FILENAME_XATTR)
    print("Prev mu: %s" % prev_mu)
    print("Prev sigma: %s" % prev_sigma)
    print("Prev filename: %s" % prev_filename)
    # Restore previous state
    set_xattr(filename, MU_XATTR, prev_mu)
    set_xattr(filename, SIGMA_XATTR, prev_sigma)
    shutil.move(filename, prev_filename)
    prev_file = get_file(prev_filename)
    if rm:
        eligible_files.insert(int(prev_index), prev_file)
    else:
        for i, file in enumerate(eligible_files):
            if file["filename"] == filename:
                eligible_files[i] = prev_file
    return prev_filename


def handle_undo(win, lose, rm=False):
    pprint(("handle_undo", win, lose))
    win = undo_update_file(win, rm)
    lose = undo_update_file(lose, rm)
    if not rm:
        undo = {"win": get_file(win), "lose": get_file(lose)}
    else:
        undo = {"win": get_file(win), "rm": get_file(lose)}
    pprint(undo)
    return undo


def load():
    try:
        dir = sys.argv[1]
    except IndexError:
        print("You must specify a directory!")
        sys.exit(1)
    filenames = list(pathlib.Path(dir).rglob("*"))
    if len(filenames) < 2:
        print("Did not find images!")
        sys.exit(1)
    for filename in filenames:
        ext = filename.suffix.lower()
        if ext not in SUPPORTED_EXTS:
            continue
        filename = str(filename)
        # print("Loading: %s" % filename)
        index = len(eligible_files)
        files_index[filename] = index
        eligible_files.append(get_file(filename))


def get_candidates():
    # Select the file with the lowest sigma (confidence) as the starting
    # candidate
    highest_sigma_file = None
    for file_dict in eligible_files:
        if highest_sigma_file is None:
            highest_sigma_file = file_dict
            continue
        if file_dict['rating'].sigma > highest_sigma_file['rating'].sigma:
            highest_sigma_file = file_dict
            continue
    # Select the file with the closest rank
    closest_mu_file = None
    lowest_mu_difference = None
    for file_dict in eligible_files:
        # Don't pit an image against itself
        if file_dict["filename"] == highest_sigma_file["filename"]:
            continue
        mu_difference = abs(
            highest_sigma_file['rating'].mu - file_dict['rating'].mu)
        if closest_mu_file is None or mu_difference < lowest_mu_difference:
            closest_mu_file = file_dict
            lowest_mu_difference = mu_difference
            continue
    candidates = [highest_sigma_file, closest_mu_file]
    return candidates


def get_unquote(param):
    value = request.args.get(param)
    if value is not None:
        value = unquote(value)
    return value


@app.route('/img')
def img():
    filename = get_unquote('filename')
    img_file = open(filename, "rb")
    mimetype = mimetypes.guess_type(filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)


@app.route('/')
def index():
    undo = None
    results = None
    unwin = get_unquote('unwin')
    unlose = get_unquote('unlose')
    unrm = get_unquote('unrm')
    if unwin is not None:
        # Undoing something takes preference
        if unlose is not None:
            undo = handle_undo(unwin, unlose)
        if unrm is not None:
            undo = handle_undo(unwin, unrm, rm=True)
    else:
        # Not undoing anything
        win = get_unquote('win')
        lose = get_unquote('lose')
        rm = get_unquote('rm')
        if win is not None:
            if lose is not None:
                results = handle_match(win, lose)
            if rm is not None:
                results = handle_match(win, rm, rm=True)
    context = {
        "undo": undo,
        "results": results,
        "candidates": get_candidates()
    }
    return flask.render_template(TEMPLATE, **context)


if __name__ == '__main__':
    load()
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if 'WERKZEUG_RUN_MAIN' not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()
