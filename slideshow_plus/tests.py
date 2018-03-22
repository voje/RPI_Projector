from core import *
import logging
import pprint
import time

log = logging.getLogger(__name__)


def t_find_usb_files(core):
    log.debug("testing core.find_usb_files()")
    log.debug(core.find_usb_files())


def t_init_files(core):
    log.debug("testing core.init_files()")
    log.debug(core.init_files())
    log.debug(pprint.pprint(core.files))


def t_display(core):
    for file in core.files:
        core.display()
        time.sleep(3)
        core.next_file()


if __name__ == "__main__":
    # Set logging preferences here, not in modules.
    logging.basicConfig(level=logging.DEBUG)

    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi",
        default_files_dir="/home/kristjan/Pictures/mock_usb/diapozitivi"
    )

    # t_find_usb_files(core)
    # t_init_files(core)
    t_display(core)
