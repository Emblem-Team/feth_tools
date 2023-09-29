from app.utils.path import (
    BIN_PATH,
    JSON_PATCHED_PATH,
    JSON_RAW_PATH,
    MODS_PATH,
    remove_files
)
from glob import glob
from os.path import join


def clear_all() -> None:
    clear_bin()
    clear_json()
    clear_mods()


def clear_bin() -> None:
    remove_files(glob(join(BIN_PATH, "*")))


def clear_json() -> None:
    remove_files(glob(join(JSON_RAW_PATH, "*.json")))
    remove_files(glob(join(JSON_PATCHED_PATH, "*.json")))


def clear_mods() -> None:
    remove_files(glob(join(MODS_PATH, "*")))
