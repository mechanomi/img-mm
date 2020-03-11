import mimetypes
import time
import os
import pathlib
import re
import shutil
import sys
import threading
import webbrowser

from flask import request

from urllib.parse import unquote

from PIL import Image

import flask
import trueskill
import xattr

from pprint import pprint

app = flask.Flask(__name__)

APP_URL = "http://127.0.0.1:5000/"
RANK_MULTIPLIER = 1000
TEMPLATE = "img-mm.tpl"
MU_XATTR = "img-mm.ts.mu"
SIGMA_XATTR = "img-mm.ts.sigma"
PREV_MU_XATTR = "img-mm.ts.mu.prev"
PREV_SIGMA_XATTR = "img-mm.ts.sigma.prev"
PREV_INDEX_XATTR = "img-mm.index.prev"
PREV_FILENAME_XATTR = "img-mm.filename.prev"
SUPPORTED_EXTS = [
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".webp",
]

src_dir = pathlib.Path(os.path.dirname(__file__))
cwd = pathlib.Path.cwd()
tmp_path = pathlib.Path("/tmp").resolve()

ALLOWED_PATHS = [src_dir, cwd, tmp_path]

eligible_imgs = []

imgs_index = {}

unrated_imgs_count = 0

total_sigma = 0


def get_img_path(img_filename):
    allowed = False
    img_path = pathlib.Path(img_filename).resolve()

    for allowed_path in ALLOWED_PATHS:
        try:
            print(allowed_path)
            print(img_path)
            img_path.relative_to(allowed_path)
            allowed = True
        except ValueError:
            continue
    if not allowed:
        raise Exception("Path not allowed.")
    return img_path


def rank(rating):
    rank = str(
        (50 * RANK_MULTIPLIER)
        - round((rating.mu - (3 * rating.sigma)) * RANK_MULTIPLIER)
    )
    return rank


def get_xattr(filename, name):
    try:
        value = xattr.getxattr(filename, name).decode("UTF8")
    except OSError:
        value = None
    return value


def set_xattr(filename, name, value):
    xattr.setxattr(filename, name, value.encode("UTF8"))


def get_img(img_path):
    img_filename = str(img_path)
    mu = get_xattr(img_filename, MU_XATTR)
    sigma = get_xattr(img_filename, SIGMA_XATTR)
    prev_mu = get_xattr(img_filename, PREV_MU_XATTR)
    prev_sigma = get_xattr(img_filename, PREV_SIGMA_XATTR)
    prev_index = get_xattr(img_filename, PREV_INDEX_XATTR)
    prev_filename = get_xattr(img_filename, PREV_FILENAME_XATTR)
    previous_rating = False
    if mu is not None or sigma is not None:
        previous_rating = True
        rating = trueskill.Rating(mu=float(mu), sigma=float(sigma))
        global total_sigma
        total_sigma+=float(sigma)
    else:
        rating = trueskill.Rating()
        global unrated_imgs_count
        unrated_imgs_count+=1
    return {
        "path": img_path,
        "filename": str(img_path),
        "mtime": os.path.getmtime(img_filename),
        "previous_rating": previous_rating,
        "rating": rating,
        "prev_mu": prev_mu,
        "prev_sigma": prev_sigma,
        "prev_index": prev_index,
        "prev_filename": prev_filename,
        "rank": rank(rating),
    }


def update_img(img_dict, rating, rm=False):
    print("Update from %s to %s" % (img_dict["rating"].mu, rating.mu))
    # Save current state
    prev_mu = str(img_dict["rating"].mu)
    prev_sigma = str(img_dict["rating"].sigma)
    prev_index = str(imgs_index[img_dict["filename"]])
    prev_filename = img_dict["filename"]
    set_xattr(img_dict["filename"], PREV_MU_XATTR, prev_mu)
    set_xattr(img_dict["filename"], PREV_SIGMA_XATTR, prev_sigma)
    set_xattr(img_dict["filename"], PREV_INDEX_XATTR, prev_index)
    set_xattr(img_dict["filename"], PREV_FILENAME_XATTR, prev_filename)
    # Update state
    set_xattr(img_dict["filename"], MU_XATTR, str(rating.mu))
    set_xattr(img_dict["filename"], SIGMA_XATTR, str(rating.sigma))
    suffix = re.split(r"^(\d+R)\s+?", img_dict["path"].name)[-1]
    new_name = "%sR %s" % (rank(rating), suffix)
    if not rm:
        new_filename = str(img_dict["path"].parent.joinpath(new_name))
    else:
        tmp_path = pathlib.PurePath("/tmp")
        new_filename = str(tmp_path.joinpath(new_name))
    shutil.move(img_dict["filename"], new_filename)
    new_file = get_img(new_filename)
    for i, img in enumerate(eligible_imgs):
        if img["filename"] == img_dict["filename"]:
            if not rm:
                eligible_imgs[i] = new_file
            else:
                del eligible_imgs[i]
    return new_file


def handle_match(win, lose, rm=False):
    pprint(("handle_match", win, lose, rm))
    try:
        win_file = get_img(win)
        lose_file = get_img(lose)
    except FileNotFoundError:
        # File has gone. User might have refreshed page after file was renamed.
        # Either way, no way to recover, so take no action.
        return
    win_rating, lose_rating = trueskill.rate_1vs1(
        win_file["rating"], lose_file["rating"]
    )
    print("Before:")
    print("  Win:  " + rank(win_file["rating"]) + " " + win_file["filename"])
    print("  Lose: " + rank(lose_file["rating"]) + " " + lose_file["filename"])
    print("After:")
    print("  Win:  " + rank(win_rating) + " " + win_file["filename"])
    print("  Lose: " + rank(lose_rating) + " " + lose_file["filename"])
    win_file = update_img(win_file, win_rating)
    lose_file = update_img(lose_file, lose_rating, rm)
    if not rm:
        results = {"win": win_file, "lose": lose_file}
    else:
        results = {"win": win_file, "rm": lose_file}
    pprint(results)
    return results


def undo_update_img(img_dict, rm=False):
    # Get previous state
    prev_mu = get_xattr(img_dict["filename"], PREV_MU_XATTR)
    prev_sigma = get_xattr(img_dict["filename"], PREV_SIGMA_XATTR)
    prev_index = get_xattr(img_dict["filename"], PREV_INDEX_XATTR)
    prev_filename = get_xattr(img_dict["filename"], PREV_FILENAME_XATTR)
    print("Prev mu: %s" % prev_mu)
    print("Prev sigma: %s" % prev_sigma)
    print("Prev filename: %s" % prev_filename)
    # Restore previous state
    set_xattr(img_dict["filename"], MU_XATTR, prev_mu)
    set_xattr(img_dict["filename"], SIGMA_XATTR, prev_sigma)
    shutil.move(img_dict["filename"], prev_filename)
    prev_img = get_img(prev_filename)
    if rm:
        eligible_imgs.insert(int(prev_index), prev_img)
    else:
        for i, img in enumerate(eligible_imgs):
            if img["filename"] == img_dict["filename"]:
                eligible_imgs[i] = prev_img
    return prev_filename


def handle_undo(win, lose, rm=False):
    pprint(("handle_undo", win, lose))
    try:
        win_dict = get_img(win)
        lose_dict = get_img(lose)
    except FileNotFoundError:
        # File has gone. User might have refreshed page after file was renamed.
        # Either way, no way to recover, so take no action.
        return
    win = undo_update_img(win_dict, rm)
    lose = undo_update_img(lose_dict, rm)
    if not rm:
        undo = {"win": get_img(win), "lose": get_img(lose)}
    else:
        undo = {"win": get_img(win), "rm": get_img(lose)}
    pprint(undo)
    return undo



def handle_rotate(rotate_img, cw=True):
    img = get_img(rotate_img)
    img_obj = Image.open(img["filename"])
    print("rotating")
    if cw:
        out = img_obj.rotate(-90)
    else:
        out = img_obj.rotate(90)
    out.save(img["filename"])


def reset():
    global eligible_imgs, imgs_index, unrated_imgs_count, total_sigma
    eligible_imgs = []
    imgs_index = {}
    unrated_imgs_count = 0
    total_sigma = 0

def load_imgs():
    reset()
    img_filenames = list(cwd.rglob("*"))
    if len(img_filenames) < 2:
        print("Did not find images!")
        sys.exit(1)
    for img_filename in img_filenames:
        ext = img_filename.suffix.lower()
        if ext not in SUPPORTED_EXTS:
            continue
        img_filename = str(img_filename)
        # print("Loading: %s" % filename)
        index = len(eligible_imgs)
        imgs_index[img_filename] = index
        eligible_imgs.append(get_img(img_filename))


def get_candidates():
    # Select the file with the lowest sigma (confidence) as the starting
    # candidate
    highest_sigma_file = None
    for img_dict in eligible_imgs:
        if highest_sigma_file is None:
            highest_sigma_file = img_dict
            continue
        if img_dict["rating"].sigma > highest_sigma_file["rating"].sigma:
            highest_sigma_file = img_dict
            continue
    # Select the file with the closest rank
    closest_mu_file = None
    lowest_mu_difference = None
    for img_dict in eligible_imgs:
        # Don't pit an image against itself
        if img_dict["filename"] == highest_sigma_file["filename"]:
            continue
        mu_difference = abs(
            highest_sigma_file["rating"].mu - img_dict["rating"].mu
        )
        if closest_mu_file is None or mu_difference < lowest_mu_difference:
            closest_mu_file = img_dict
            lowest_mu_difference = mu_difference
            continue
    candidates = [highest_sigma_file, closest_mu_file]
    return candidates

def get_arg(param):
    param = request.args.get(param)
    if not param:
        return None
    return param

def get_arg_img_path(param):
    img_filename = request.args.get(param)
    if not img_filename:
        return None
    img_path = get_img_path(unquote(img_filename))
    return img_path


@app.route("/img")
def img():
    img_path = get_arg_img_path("filename")
    if not img_path:
        raise Exception("Not a valid path")
    img_filename = str(img_path)
    img_file = open(img_filename, "rb")
    mimetype = mimetypes.guess_type(img_filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)


@app.route("/")
def index():
    load_imgs()
    undo = None
    results = None
    rotate_img = get_arg_img_path("rotate_img")
    if rotate_img is not None:
        print("rotate_img")
        # Rotating something takes preference
        direction = get_arg("direction")
        print(direction)
        if direction == "cw":
            print("abt to handle rotate")
            handle_rotate(rotate_img)
        if direction == "ccw":
            print("abt to handle rotate")
            handle_rotate(rotate_img, False)
    else:
        unwin = get_arg_img_path("unwin")
        unlose = get_arg_img_path("unlose")
        unrm = get_arg_img_path("unrm")
        if unwin is not None:
            # Undoing something takes preference
            if unlose is not None:
                undo = handle_undo(unwin, unlose)
            if unrm is not None:
                undo = handle_undo(unwin, unrm, rm=True)
        else:
            # Not undoing anything
            win = get_arg_img_path("win")
            lose = get_arg_img_path("lose")
            rm = get_arg_img_path("rm")
            if win is not None:
                if lose is not None:
                    results = handle_match(win, lose)
                if rm is not None:
                    results = handle_match(win, rm, rm=True)
    imgs_count = len(eligible_imgs)
    unrated_pct = round(unrated_imgs_count/imgs_count * 100)
    avg_sigma = round(total_sigma / imgs_count, 2)
    context = {
        "src_dir": src_dir,
        "ts": time.time(),
        "imgs_count": imgs_count,
        "unrated_imgs_count": unrated_imgs_count,
        "unrated_pct": unrated_pct,
        "avg_sigma": avg_sigma,
        "undo": undo,
        "results": results,
        "candidates": get_candidates(),
    }
    return flask.render_template(TEMPLATE, **context)


if __name__ == "__main__":
    # load_imgs()
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if "WERKZEUG_RUN_MAIN" not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()
