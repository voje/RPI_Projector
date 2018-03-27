# -*- coding: utf-8 -*-

# Core application for slideshow_plus.
# Rule of thumb: always use absolute paths.
import getpass
from os import listdir, system
from os.path import isfile, join, basename, dirname, exists, splitext
import re
import magic
import logging
from time import time
from slideshow_plus.projector import pjlink

log = logging.getLogger(__name__)

get_numbers = re.compile(r'\d+')


class Core():
    def __init__(
        self, media_root_dir=None, files_dir_basename=None
    ):
        if media_root_dir is None:
            raise Exception("core parameter missing: media_root_dir")
        if files_dir_basename is None:
            raise Exception("core parameter missing: files_dir_basename")
        self.media_root_dir = media_root_dir
        self.static_files_dir = join(
            dirname(__file__), "core_static")
        self.files_dir_basename = files_dir_basename or "diapozitivi"

        # Add default files.
        self.reserved_filenames = ["r_blank.pdf"]

        # File indexing.
        # File unique ID is the list index in self.files.
        self.files = []
        self.current_idx = 0
        self.idx_map = {}  # filename number to list index
        self.idx_history = []
        self.current_hist_idx = -1
        self.HIST_LEN = 20

        # Function order is important.
        self.find_usb_files_wrapper()
        self.convert_files()
        self.init_files()

        self.blank = False
        self.projector = pjlink.Pjlink()

    def convert_files(self):
        # If not pdf, convert to pdf and store in converted_ folder.
        tstart = time()
        mass_convert = "{}/core_static/mass_convert.sh".format(
            dirname(__file__))
        system(("bash {} {} {}").format(
            mass_convert,
            self.files_dir,
            self.converted_files_dir
        ))
        log.info("ran mass_convert.sh in {:.2f}s".format(
            time() - tstart))

    def init_files(self):
        # Reset values
        self.files = []
        self.current_idx = 0
        self.idx_map = {}  # filename number to list index
        self.idx_history = []
        self.current_hist_idx = -1

        ordered = []
        unordered = []
        # Read user files.
        for filename in [
            fn for fn in listdir(self.files_dir)
            if isfile(join(self.files_dir, fn))
        ]:
            filepath = None
            if (
                magic.from_file(join(self.files_dir, filename))[:3] == "PDF"
            ):
                filepath = join(self.files_dir, filename)
            else:
                converted_filename = join(
                    self.converted_files_dir,
                    splitext(basename(filename))[0] + ".pdf"
                )
                if isfile(converted_filename):
                    filepath = join(
                        self.converted_files_dir,
                        converted_filename
                    )
                else:
                    continue
            while filename in self.reserved_filenames:
                filename = "_" + filename
            entry = {
                "filename": filename,
                "filepath": filepath,
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
            log.debug(entry)
        if not self.files:
            log.error("Empty self.files list. Exiting.")
            exit(1)
        return True

    def display(self, add_to_history=None):
        if add_to_history is None:
            add_to_history = True
        blank_filepath = join(self.static_files_dir, "r_slides/r_blank.pdf")
        filepath = self.files[self.current_idx]["filepath"]
        if self.blank:
            filepath = blank_filepath
        elif not isfile(filepath):
            log.warning("file not found: {}")
            filepath = blank_filepath
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
        self.idx_history = self.idx_history[:-1]
        self.current_hist_idx = len(self.idx_history) - 1

    def toggle_blank(self):
        self.blank = not self.blank
        self.display(add_to_history=False)

    def special_command(self, command):
        log.info("special_command:{}".format(command))
        if command == "0001":
            self.find_usb_files_wrapper()
            self.init_files()
            self.display()

    def find_usb_files_wrapper(self):
        self.files_dir = self.find_usb_files()[0]
        self.converted_files_dir = join(
            dirname(self.files_dir),
            "converted_" + self.files_dir_basename
        )
        log.info("found files in {}".format(self.files_dir))

    def find_usb_files(self):
        # Returns (path_fo_files, bool)
        # bool = True if files were found on USB,
        # bool = False if files are from default fallback folder.
        # Requires system to automount USB. !!!
        default_dir = join(
            self.static_files_dir, self.files_dir_basename
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
