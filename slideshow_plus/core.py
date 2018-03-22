# -*- coding: utf-8 -*-

# Core application for slideshow_plus.
import getpass
from os import listdir, system
from os.path import isfile, join, basename, realpath, dirname, exists
import re

import logging
log = logging.getLogger(__name__)

get_numbers = re.compile(r'\d+')


class Core():
    def __init__(
        self, media_root_dir=None, files_dir_basename=None,
        default_files_dir=None
    ):
        if media_root_dir is None:
            raise Exception("core parameter missing: media_root_dir")
        if files_dir_basename is None:
            raise Exception("core parameter missing: files_dir_basename")
        self.media_root_dir = media_root_dir
        self.files_dir_basename = files_dir_basename  # e.g. diapozitivi
        self.default_files_dir = default_files_dir or "default_files"
        self.files_dir = None

        # File indexing.
        self.files = []
        self.current_idx = 0
        self.idx_map = {}
        self.idx_history = []
        self.HIST_LEN = 20
        self.init_files()

    def init_files(self):
        # Add default files.
        reserved = ["r_blank"]
        ordered = []
        unordered = []
        # Read user files.
        self.files_dir, found = self.find_usb_files()
        if not found:
            log.debug("init_files():no USB path found, fallback to {}".format(
                self.default_files_dir))
        for filename in [
            fn for fn in listdir(self.files_dir)
            if isfile(join(self.files_dir, fn))
        ]:
            while filename in reserved:
                filename = "_" + filename
            entry = {
                "filename": filename,
                "number": None
            }
            nu = get_numbers.findall(filename)
            if nu:
                entry["number"] = str(int(nu[0]))
                ordered.append(entry)
            else:
                unordered.append(entry)
        ordered = sorted(ordered, key=lambda x: int(x["number"]))
        self.files = ordered + unordered
        for i, entry in enumerate(self.files):
            if entry["number"] is not None:
                self.idx_map[entry["number"]] = i
        if not self.files:
            log.error("Empty self.files list. Exiting.")
            exit(1)
        return True

    def display(self):
        file = self.files[self.current_idx]
        filepath = join(self.files_dir, file["filename"])
        log.debug("display():displaying current file: {}".format(filepath))
        self.idx_history.append(self.current_idx)
        self.idx_history = self.idx_history[-self.HIST_LEN:]
        log.debug("display():self.history:{}".format(self.idx_history))
        system("xpdf -fullscreen -remote my_server '{}' &".format(filepath))

    def next_file(self):
        self.current_idx += 1
        if self.current_idx >= len(self.files):
            self.current_idx = len(self.files) - 1

    def prev_file(self):
        self.current_idx -= 1
        if self.current_idx <= 0:
            self.current_idx = 0

    def next_hist_file(self):
        self.current_hist_idx += 1
        if self.current_hist_idx >= self.HIST_LEN:
            self.current_hist_idx = self.HIST_LEN - 1

    def prev_hist_file(self):
        self.current_hist_idx -= 1
        if self.current_hist_idx < 0:
            self.current_hist_idx = 0

    def find_usb_files(self):
        # Returns (path_fo_files, bool)
        # bool = True if files were found on USB,
        # bool = False if files are from default fallback folder.
        # Requires system to automount USB. !!!
        default_dir = join(
            (dirname(realpath(__file__))), self.default_files_dir
        )
        media_user_dir = join(self.media_root_dir, getpass.getuser())
        log.debug("looking for media in [{}]".format(media_user_dir))
        if not exists(media_user_dir):
            return (default_dir, False)
        for usb_dir in [
            join(media_user_dir, x) for x in listdir(media_user_dir)
            if not isfile(join(media_user_dir, x))
        ]:
            for files_dir in [
                join(usb_dir, x) for x in listdir(usb_dir)
                if not isfile(join(usb_dir, x))
            ]:
                if basename(files_dir) == self.files_dir_basename:
                    return (files_dir, True)
        return (default_dir, False)
