# -*- coding: utf-8 -*-

# Core application for slideshow_plus.
import getpass
from os import listdir, system
from os.path import isfile, join, basename, realpath, dirname, exists
import re
import magic
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

        # Add default files.
        self.reserved_filenames = ["r_blank"]

        # File indexing.
        # File unique ID is the list index in self.files.
        self.files = []
        self.current_idx = 0
        self.idx_map = {}  # filename number to list index
        self.idx_history = []
        self.current_hist_idx = -1
        self.HIST_LEN = 3
        self.init_files()

    def init_files(self):
        ordered = []
        unordered = []
        # Read user files.
        self.files_dir, found = self.find_usb_files()
        if not found:
            log.debug("init_files():no USB path found, fallback to {}".format(
                self.default_files_dir))
        for filename in [
            fn for fn in listdir(self.files_dir)
            if isfile(join(self.files_dir, fn)) and
            magic.from_file(join(self.files_dir, fn))[:3] == "PDF"
        ]:
            while filename in self.reserved_filenames:
                filename = "_" + filename
            entry = {
                "filename": filename,
                "number": None,  # from filename
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

    def display(self, add_to_history=None):
        if add_to_history is None:
            add_to_history = True
        file = self.files[self.current_idx]
        filepath = join(self.files_dir, file["filename"])
        log.debug("display():displaying current file: {}".format(filepath))
        if add_to_history:
            if (
                len(self.idx_history) == 0 or
                (self.idx_history[-1] != self.current_idx)
            ):
                # TODO .. this event doesn't fire...
                self.idx_history.append(self.current_idx)
                self.idx_history = self.idx_history[-self.HIST_LEN:]
                self.current_hist_idx = len(self.idx_history) - 1
                log.debug("display():self.history:{}".format(self.idx_history))
        # -fullscreen
        system((
            "xpdf -remote my_server '{}' "
            ">/dev/null 2>&1 &".format(filepath)
        ))

    def next_file(self):
        self.current_idx += 1
        if self.current_idx >= len(self.files):
            self.current_idx = len(self.files) - 1

    def prev_file(self):
        self.current_idx -= 1
        if self.current_idx <= 0:
            self.current_idx = 0

    def file_by_number(self, number):
        if number == "":
            return False
        str_num = str(int(number))
        if str_num not in self.idx_map:
            return False
        self.current_idx = self.idx_map[str_num]
        return True

    # Todo: calling add_to_history in display.
    def next_hist_file(self):
        self.current_hist_idx += 1
        if self.current_hist_idx >= self.HIST_LEN:
            self.current_hist_idx = self.HIST_LEN - 1
        self.current_idx = self.idx_history[self.current_hist_idx]

    def prev_hist_file(self):
        self.current_hist_idx -= 1
        if self.current_hist_idx < 0:
            self.current_hist_idx = 0
        self.current_idx = self.idx_history[self.current_hist_idx]

    def del_hist_file(self):
        self.idx_history = self.idx_history[:-1]
        self.current_hist_idx = len(self.idx_history) - 1

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
