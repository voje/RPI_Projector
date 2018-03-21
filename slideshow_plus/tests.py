from core import *
import logging

log = logging.getLogger(__name__)


def t_find_usb_files(core):
    log.debug("testing core.find_usb_files()")
    log.debug(core.find_usb_files())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename="./logging.log", level=logging.DEBUG)
    # logging levels: NONE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi"
    )

    t_find_usb_files(core)
