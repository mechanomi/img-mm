import time
import mimetypes

import flask

from imgmm import app
from imgmm import core
from imgmm import helpers


@app.route("/img")
def img():
    img_path = helpers.get_arg_img_path("filename")
    if not img_path:
        raise Exception("Not a valid path")
    img_filename = str(img_path)
    img_file = open(img_filename, "rb")
    mimetype = mimetypes.guess_type(img_filename)[0]
    return flask.send_file(img_file, mimetype=mimetype)


@app.route("/")
def index():
    core.load_imgs()
    undo = None
    results = None
    rotate_img = helpers.get_arg_img_path("rotate_img")
    if rotate_img is not None:
        print("rotate_img")
        # Rotating something takes preference
        direction = helpers.get_arg("direction")
        print(direction)
        if direction == "cw":
            print("abt to handle rotate")
            core.handle_rotate(rotate_img)
        if direction == "ccw":
            print("abt to handle rotate")
            core.handle_rotate(rotate_img, False)
    else:
        unwin = helpers.get_arg_img_path("unwin")
        unlose = helpers.get_arg_img_path("unlose")
        unrm = helpers.get_arg_img_path("unrm")
        if unwin is not None:
            # Undoing something takes preference
            if unlose is not None:
                undo = core.handle_undo(unwin, unlose)
            if unrm is not None:
                undo = core.handle_undo(unwin, unrm, rm=True)
        else:
            # Not undoing anything
            win = helpers.get_arg_img_path("win")
            lose = helpers.get_arg_img_path("lose")
            rm = helpers.get_arg_img_path("rm")
            if win is not None:
                if lose is not None:
                    results = core.handle_match(win, lose)
                if rm is not None:
                    results = core.handle_match(win, rm, rm=True)
    imgs_count = len(core.eligible_imgs)
    unrated_pct = round((imgs_count - core.unrated_imgs_count) / imgs_count * 100)
    avg_sigma = round(core.total_sigma / imgs_count, 2)
    context = {
        "src_dir": core.src_dir,
        "ts": time.time(),
        "imgs_count": imgs_count,
        "unrated_imgs_count": core.unrated_imgs_count,
        "unrated_pct": unrated_pct,
        "avg_sigma": avg_sigma,
        "undo": undo,
        "results": results,
        "candidates": core.get_candidates(),
    }
    return flask.render_template(core.TEMPLATE, **context)
