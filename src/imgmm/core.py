import os
import pathlib
import re
import shutil
import sys
import threading
import webbrowser

from PIL import Image

import flask
import trueskill
import xattr

from pprint import pprint

APP_URL = "http://127.0.0.1:5000/"
RANK_MULTIPLIER = 1000
TEMPLATE = "imgmm.tpl"
SUPPORTED_EXTS = [
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".webp",
]


def get_xattr(filename, name):
    try:
        value = xattr.getxattr(filename, name).decode("UTF8")
    except OSError:
        value = None
    return value


def set_xattr(filename, name, value):
    xattr.setxattr(filename, name, value.encode("UTF8"))

class RankedImage(object):

    MU_XATTR = "imgmm.ts.mu"
    SIGMA_XATTR = "imgmm.ts.sigma"
    PREV_MU_XATTR = "imgmm.ts.mu.prev"
    PREV_SIGMA_XATTR = "imgmm.ts.sigma.prev"
    PREV_INDEX_XATTR = "imgmm.index.prev"
    PREV_FILENAME_XATTR = "imgmm.filename.prev"

    path = None
    filename = None
    mtime = None
    prev_mu = None
    prev_sigma = None
    prev_index = None
    prev_filename = None
    previous_rating = None
    rating = None
    rank = None

    def __init__(self, path):
        self.path = path
        self.filename = str(self.path)
        self.mtime = os.path.getmtime(self.filename)
        mu = get_xattr(self.filename, self.MU_XATTR)
        sigma = get_xattr(self.filename, self.SIGMA_XATTR)
        self.prev_mu = get_xattr(self.filename, self.PREV_MU_XATTR)
        self.prev_sigma = get_xattr(self.filename, self.PREV_SIGMA_XATTR)
        self.prev_index = get_xattr(self.filename, self.PREV_INDEX_XATTR)
        self.prev_filename = get_xattr(self.filename, self.PREV_FILENAME_XATTR)
        self.previous_rating = False
        if mu is not None or sigma is not None:
            self.previous_rating = True
            self.set_rating(trueskill.Rating(mu=float(mu), sigma=float(sigma)))
        else:
            self.set_rating(trueskill.Rating())

    def set_rating(self, rating):
        self.rating = rating
        self.rank = str(
            (50 * RANK_MULTIPLIER)
            - round((rating.mu - (3 * rating.sigma)) * RANK_MULTIPLIER)
        )

    def update(self, index, rating, rm=False):
        print("Update from %s to %s" % (self.rating.mu, rating.mu))
        # Save current state
        set_xattr(self.filename, self.PREV_MU_XATTR, str(self.rating.mu))
        set_xattr(self.filename, self.PREV_SIGMA_XATTR, str(self.rating.sigma))
        set_xattr(self.filename, self.PREV_INDEX_XATTR, index)
        set_xattr(self.filename, self.PREV_FILENAME_XATTR, self.filename)
        # Update state
        self.set_rating(rating)
        set_xattr(self.filename, self.MU_XATTR, str(rating.mu))
        set_xattr(self.filename, self.SIGMA_XATTR, str(rating.sigma))
        suffix = re.split(r"^(\d+R)\s+?", self.path.name)[-1]
        new_name = "%sR %s" % (self.rank, suffix)
        if not rm:
            new_filename = str(self.path.parent.joinpath(new_name))
        else:
            tmp_path = pathlib.PurePath("/tmp")
            new_filename = str(tmp_path.joinpath(new_name))
        shutil.move(self.filename, new_filename)
        self.__init__(pathlib.Path(new_filename))


class FileSystem(object):

    src_dir = None
    cwd = None
    tmp_path = None
    allowed_paths = None
    eligible_imgs = None
    imgs_index = None
    unrated_imgs_count = None
    total_sigma = None


    def __init__(self):
        self.src_dir = pathlib.Path(os.path.dirname(__file__))
        self.cwd = pathlib.Path.cwd()
        self.tmp_path = pathlib.Path("/tmp").resolve()
        self.allowed_paths = [self.src_dir, self.cwd, self.tmp_path]
        self.eligible_imgs = []
        self.imgs_index = {}
        self.unrated_imgs_count = 0
        self.total_sigma = 0

    def reset(self):
        eligible_imgs = []
        imgs_index = {}
        unrated_imgs_count = 0
        total_sigma = 0


    def get_img(self, img_path):
        img = RankedImage(img_path)
        if img.previous_rating:
            self.total_sigma+=img.rating.sigma
        else:
            self.unrated_imgs_count+=1
        return img

    def get_img_path(self, img_filename):
        allowed = False
        img_path = pathlib.Path(img_filename).resolve()
        for allowed_path in self.allowed_paths:
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


    def update_img(self, img, rating, rm=False):
        index = str(self.imgs_index[img.filename])
        img.update(index, rating, rm)
        for i, eligible_img in enumerate(self.eligible_imgs):
            if eligible_img.filename == img.prev_filename:
                if not rm:
                    self.eligible_imgs[i] = img
                else:
                    del self.eligible_imgs[i]


    def scan(self):
        self.reset()
        img_filenames = list(self.cwd.rglob("*"))
        if len(img_filenames) < 2:
            print("Did not find images!")
            sys.exit(1)
        for img_filename in img_filenames:
            ext = img_filename.suffix.lower()
            if ext not in SUPPORTED_EXTS:
                continue
            img_filename = str(img_filename)
            # print("Loading: %s" % filename)
            index = len(self.eligible_imgs)
            self.imgs_index[img_filename] = index
            self.eligible_imgs.append(self.get_img(img_filename))


    def get_candidates(self):
        # Select the file with the lowest sigma (confidence) as the starting
        # candidate
        highest_sigma_file = None
        for img_dict in self.eligible_imgs:
            if highest_sigma_file is None:
                highest_sigma_file = img_dict
                continue
            if img_dict.rating.sigma > highest_sigma_file.rating.sigma:
                highest_sigma_file = img_dict
                continue
        # Select the file with the closest rank
        closest_mu_file = None
        lowest_mu_difference = None
        for img_dict in self.eligible_imgs:
            # Don't pit an image against itself
            if img_dict.filename == highest_sigma_file.filename:
                continue
            mu_difference = abs(
                highest_sigma_file.rating.mu - img_dict.rating.mu
            )
            if closest_mu_file is None or mu_difference < lowest_mu_difference:
                closest_mu_file = img_dict
                lowest_mu_difference = mu_difference
                continue
        candidates = [highest_sigma_file, closest_mu_file]
        return candidates

    def handle_match(self, win, lose, rm=False):
        pprint(("handle_match", win, lose, rm))
        try:
            win_file = self.get_img(win)
            lose_file = self.get_img(lose)
        except FileNotFoundError:
            # File has gone. User might have refreshed page after file was renamed.
            # Either way, no way to recover, so take no action.
            return
        win_rating, lose_rating = trueskill.rate_1vs1(
            win_file.rating, lose_file.rating
        )
        self.update_img(win_file, win_rating)
        self.update_img(lose_file, lose_rating, rm)
        if not rm:
            results = {"win": win_file, "lose": lose_file}
        else:
            results = {"win": win_file, "rm": lose_file}
        pprint(results)
        return results


    def undo_update_img(self, img_dict, rm=False):
        # Get previous state
        prev_mu = get_xattr(img_dict.filename, PREV_MU_XATTR)
        prev_sigma = get_xattr(img_dict.filename, PREV_SIGMA_XATTR)
        prev_index = get_xattr(img_dict.filename, PREV_INDEX_XATTR)
        prev_filename = get_xattr(img_dict.filename, PREV_FILENAME_XATTR)
        print("Prev mu: %s" % prev_mu)
        print("Prev sigma: %s" % prev_sigma)
        print("Prev filename: %s" % prev_filename)
        # Restore previous state
        set_xattr(img_dict.filename, MU_XATTR, prev_mu)
        set_xattr(img_dict.filename, SIGMA_XATTR, prev_sigma)
        shutil.move(img_dict.filename, prev_filename)
        prev_img = self.get_img(prev_filename)
        if rm:
            self.eligible_imgs.insert(int(prev_index), prev_img)
        else:
            for i, img in enumerate(self.eligible_imgs):
                if img.filename == img_dict.filename:
                    self.eligible_imgs[i] = prev_img
        return prev_filename


    def handle_undo(self, win, lose, rm=False):
        pprint(("handle_undo", win, lose))
        try:
            win_dict = self.get_img(win)
            lose_dict = self.get_img(lose)
        except FileNotFoundError:
            # File has gone. User might have refreshed page after file was renamed.
            # Either way, no way to recover, so take no action.
            return
        win = self.undo_update_img(win_dict, rm)
        lose = self.undo_update_img(lose_dict, rm)
        if not rm:
            undo = {"win": self.get_img(win), "lose": self.get_img(lose)}
        else:
            undo = {"win": self.get_img(win), "rm": self.get_img(lose)}
        pprint(undo)
        return undo


    def handle_rotate(self, rotate_img, cw=True):
        img = self.get_img(rotate_img)
        img_obj = Image.open(img.filename)
        print("rotating")
        if cw:
            out = img_obj.rotate(-90)
        else:
            out = img_obj.rotate(90)
        out.save(img.filename)
