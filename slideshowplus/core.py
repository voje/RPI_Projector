# -*- coding: utf-8 -*-

# Core application for slideshowplus.
# Rule of thumb: always use absolute paths.
import getpass
import os
from os.path import isfile, join, basename, dirname, exists
import re
import logging
from time import time
# from slideshowplus.projector import viewsonic  # specific for poljane
from slideshowplus.projector import pjlink
from pathlib import Path

log = logging.getLogger(__name__)

get_numbers = re.compile(r'\d+')


class Core():
    def __init__(
        self, media_root_dir=None, files_dir_basename=None,
        no_display=None
    ):
        if media_root_dir is None:
            raise Exception("core parameter missing: media_root_dir")
        if files_dir_basename is None:
            raise Exception("core parameter missing: files_dir_basename")
        self.no_display = no_display  # Debug mode with xpdf off.
        if no_display is None:
            self.no_display = False
        self.media_root_dir = media_root_dir
        self.files_dir_basename = files_dir_basename or "diapozitivi"

        self.core_static = join(
            dirname(__file__), "core_static")

        # Add default files.
        self.reserved_filenames = ["r_blank.pdf"]

        # File indexing.
        # File unique ID is the list index in self.files.
        self.files = []
        self.current_idx = -1
        self.idx_map = {}  # filename number to list index
        self.idx_history = []
        self.current_hist_idx = -1
        self.HIST_LEN = 20

        self.projector = pjlink.Pjlink()
        self.blank = False
        self.last_displayed_path = join(
            self.core_static, "r_slides/r_blank.pdf")

        # Function order is important.
        self.find_usb_files_wrapper()
        self.init_files()
        self.display_index()
        log.debug("Core ready.")

    def init_files(self):
        # Reset values
        self.files = []
        self.current_idx = -1
        self.idx_map = {}  # filename number to list index
        self.idx_history = []
        self.current_hist_idx = -1

        ordered = []
        unordered = []
        # Read user files.
        for filename in [
            fn for fn in os.listdir(self.files_dir)
            if isfile(join(self.files_dir, fn))
        ]:
            while filename in self.reserved_filenames:
                filename = "_" + filename
            entry = {
                "filename": filename,
                "filepath": join(self.files_dir, filename),
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
            # log.debug(entry)
        if not self.files:
            log.error("Empty self.files list. Exiting.")
            exit(1)
        return True

    def gen_pdf(self, text, filename):
        filepath = join(self.core_static, "tmp_files", filename)
        log.info("gen_pdf: {}".format(filepath))
        status = os.system("echo '{}' | paps | ps2pdf -> {}".format(
            text, filepath))  # should be blocking
        return (True if status == 0 else False)

    def display_index(self):
        filename = "index.pdf"
        filepath = join(self.core_static, "tmp_files", filename)
        text = "Pot do datotek:\n{}\n\nIndeks:\n------\n".format(
            self.files_dir)
        for i, f in enumerate(self.files):
            if i == 50:
                text += "..."
                break
            text += "[{:^4}] {}\n".format(f["number"] or "", f["filename"])
        if self.gen_pdf(text, filename):
            wait = time()
            while not isfile(filepath):
                if time() - wait > 5:
                    log.error("display_index failed")
                    return
            self.low_display(filepath)

    def low_display(self, filepath):
        if filepath is None:
            filepath = self.last_displayed_path
        log.debug("low_display():{}".format(filepath))
        if self.blank:
            self.blanked = filepath
            filepath = join(self.core_static, "r_slides/r_blank.pdf")
        else:
            self.blanked = None
        # if self.no_display:
        #     return
        scall = "{}/bash_scripts/display_any.sh \"{}\"".format(self.core_static, filepath)
        log.debug(scall)
        os.system(scall)

    def display(self, add_to_history=None):
        if add_to_history is None:
            add_to_history = True
        filepath = self.get_current_file().get("filepath")
        if filepath is None:
            log.warning("display(): No file currently selected.")
            return
        elif not isfile(filepath):
            log.error("display(): File not found: {}".format(filepath))
            return

        if add_to_history:
            if (
                len(self.idx_history) == 0 or
                (self.idx_history[-1] != self.current_idx)
            ):
                self.idx_history.append(self.current_idx)
                self.idx_history = self.idx_history[-self.HIST_LEN:]
                self.current_hist_idx = len(self.idx_history) - 1
                log.debug("display():self.history:{}".format(self.idx_history))
        if self.blank:
            filepath = join(self.core_static, "r_slides/r_blank.pdf")
        self.low_display(filepath)

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

    def next_hist_file(self):
        if not len(self.idx_history):
            return False
        self.current_hist_idx += 1
        if self.current_hist_idx >= len(self.idx_history):
            self.current_hist_idx = len(self.idx_history) - 1
        self.current_idx = self.idx_history[self.current_hist_idx]

    def prev_hist_file(self):
        if not len(self.idx_history):
            return False
        self.current_hist_idx -= 1
        if self.current_hist_idx < 0:
            self.current_hist_idx = 0
        self.current_idx = self.idx_history[self.current_hist_idx]

    def del_hist_file(self):
        # Remove last index from history.
        log.debug("before_del: {}".format(self.idx_history))
        self.idx_history = self.idx_history[:-1]
        try:
            self.current_idx = self.idx_history[-1]
        except LookupError:
            log.info("History is empty.")
        log.debug("after_del: {}".format(self.idx_history))

    def set_blank(self, blank_on):
        if blank_on:
            self.blank = True
        else:
            self.blank = False
        self.display(add_to_history=False)

    def special_command(self, command):
        log.info("special_command:{}".format(command))
        if command == "0001":
            self.find_usb_files_wrapper()
            self.init_files()
            self.display_index()
        elif command == "0002":
            self.display_index()

    def find_usb_files_wrapper(self):
        self.files_dir = self.find_usb_files()[0]
        log.info("found files in {}".format(self.files_dir))

    def find_usb_files(self):
        # Returns (path_fo_files, bool)
        # bool = True if files were found on USB,
        # bool = False if files are from default fallback folder.
        # Requires system to automount USB. !!!
        default_dir = join(
            self.core_static, self.files_dir_basename
        )
        media_user_dir = join(self.media_root_dir, getpass.getuser())

        for filename in Path(media_user_dir).rglob("*"):
            if filename.is_dir() and filename.name == self.files_dir_basename:
                log.info("Found media in {}".format(filename))
                return ((str(filename), True))
        return (default_dir, False)

    def get_current_file(self):
        if self.current_idx >= 0:
            return self.files[self.current_idx]
        return {"filename": None, "filepath": None, "number": -2}
