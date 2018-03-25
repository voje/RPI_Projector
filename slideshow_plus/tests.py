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
    for i in range(len(core.files) + 2):
        core.display()
        time.sleep(1)
        core.next_file()

    for i in range(len(core.files) + 2):
        core.display()
        time.sleep(1)
        core.prev_file()

    time.sleep(2)

    for i in range(core.HIST_LEN + 2):
        core.display(add_to_history=False)
        time.sleep(1)
        core.prev_hist_file()

    for i in range(core.HIST_LEN + 2):
        core.display(add_to_history=False)
        time.sleep(1)
        core.next_hist_file()

    time.sleep(2)

    core.file_by_number("0")
    core.display()
    time.sleep(1)

    core.file_by_number("-1")
    core.display()
    time.sleep(1)

    core.file_by_number("2")
    core.display()
    time.sleep(1)

    core.file_by_number(101)
    core.display()
    time.sleep(1)

    core.file_by_number(33)
    core.display()
    time.sleep(1)

    time.sleep(2)

    for i in range(core.HIST_LEN + 2):
        core.display(add_to_history=False)
        time.sleep(1)
        core.prev_hist_file()


if __name__ == "__main__":
    # Set logging preferences here, not in modules.
    # logging.basicConfig(filename="debugging.log", level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi"
    )

    # t_find_usb_files(core)
    # t_init_files(core)
    # t_display(core)
