from urllib.parse import unquote

from flask import request

from imgmm import core

def get_arg(param):
    param = request.args.get(param)
    if not param:
        return None
    return param

def get_arg_img_path(fs, param):
    img_filename = request.args.get(param)
    if not img_filename:
        return None
    img_path = fs.get_img_path(unquote(img_filename))
    return img_path
