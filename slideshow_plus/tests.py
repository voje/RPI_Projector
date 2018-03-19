from core import *


def t_find_usb_files(core):
    print("testing core.find_usb_files()")
    print(core.find_usb_files())


if __name__ == "__main__":
    core = Core(
        media_root_dir="/run/media",
        files_dir_basename="diapozitivi"
    )

    t_find_usb_files(core)
