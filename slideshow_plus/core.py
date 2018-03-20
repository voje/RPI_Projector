# Core application for slideshow_plus.
import getpass
from os import listdir
from os.path import isfile, join, basename, realpath, dirname, exists


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
        self.files_dir_basename = files_dir_basename
        self.default_files_dir = default_files_dir or "default_files"
        self.files = {}
        self.current_file = {}

    def find_usb_files(self):
        # Returns (path_fo_files, bool)
        # bool = True if files were found on USB,
        # bool = False if files are from default fallback folder.
        # Requires system to automount USB. !!!

        default_dir = join(
            (dirname(realpath(__file__))), self.default_files_dir
        )

        media_user_dir = join(self.media_root_dir, getpass.getuser())
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
        # default
        return (default_dir, False)
