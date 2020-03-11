import time
import mimetypes

import flask

from imgmm import app
from imgmm import core
from imgmm import helpers


@app.route("/img")
def img():
    fs = core.FileSystem()
    img_path = helpers.get_arg_img_path(fs, "filename")
    if not img_path:
        raise Exception("Not a valid path")
    img_filename = str(img_path)
    img_file = open(img_filename, "rb")
    mimetype = mimetypes.guess_type(img_filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)


@app.route("/")
def index():
    fs = core.FileSystem()
    fs.scan()
    undo = None
    results = None
    rotate_img = helpers.get_arg_img_path(fs, "rotate_img")
    if rotate_img is not None:
        print("rotate_img")
        # Rotating something takes preference
        direction = helpers.get_arg("direction")
        print(direction)
        if direction == "cw":
            print("abt to handle rotate")
            fs.handle_rotate(rotate_img)
        if direction == "ccw":
            print("abt to handle rotate")
            fs.handle_rotate(rotate_img, False)
    else:
        unwin = helpers.get_arg_img_path(fs, "unwin")
        unlose = helpers.get_arg_img_path(fs, "unlose")
        unrm = helpers.get_arg_img_path(fs, "unrm")
        if unwin is not None:
            # Undoing something takes preference
            if unlose is not None:
                undo = fs.handle_undo(unwin, unlose)
            if unrm is not None:
                undo = fs.handle_undo(unwin, unrm, rm=True)
        else:
            # Not undoing anything
            win = helpers.get_arg_img_path(fs, "win")
            lose = helpers.get_arg_img_path(fs, "lose")
            rm = helpers.get_arg_img_path(fs, "rm")
            if win is not None:
                if lose is not None:
                    results = fs.handle_match(win, lose)
                if rm is not None:
                    results = fs.handle_match(win, rm, rm=True)
    imgs_count = len(fs.eligible_imgs)
    unrated_pct = round((imgs_count - fs.unrated_imgs_count) / imgs_count * 100)
    avg_sigma = round(fs.total_sigma / imgs_count, 2)
    context = {
        "src_dir": fs.src_dir,
        "ts": time.time(),
        "imgs_count": imgs_count,
        "unrated_imgs_count": fs.unrated_imgs_count,
        "unrated_pct": unrated_pct,
        "avg_sigma": avg_sigma,
        "undo": undo,
        "results": results,
        "candidates": fs.get_candidates(),
    }
    return flask.render_template(core.TEMPLATE, **context)
