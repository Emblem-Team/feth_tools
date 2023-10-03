from os import remove
from os.path import join, normpath, basename, splitext
from colorama import Fore
from colorama import Style
from glob import glob

DATA_PATH = "data"
DATA0_PATH = join(DATA_PATH, "DATA0.bin")
DATA1_PATH = join(DATA_PATH, "DATA1.bin")
BIN_PATH = join(DATA_PATH, "bin")
PATCHES_PATH = join(DATA_PATH, "patches")
INFO0_PATH = join(PATCHES_PATH, "INFO0.bin")
JSON_PATH = join(DATA_PATH, "json")
JSON_RAW_PATH = join(JSON_PATH, "raw")
JSON_PATCHED_PATH = join(JSON_PATH, "patched")
CSV_PATH = join(DATA_PATH, "csv")
BUNDLE_PATH = join(CSV_PATH, "bundle.csv")
VARS_PATH = join(CSV_PATH, "vars.csv")
FIXES_PATH = join(CSV_PATH, "fixes.csv")
MODS_PATH = join(DATA_PATH, "mods")
GRAPHIC_PATH = join(DATA_PATH, "graphic")
TUTORIALS_PATH = join(GRAPHIC_PATH, "tutorials")
TUTORIALS_BIN_PATH = join(BIN_PATH, "6131")


def get_mods_path(index: int | str) -> str:
    return join(MODS_PATH, str(index))


def get_binary_path(index: int | str) -> str:
    return join(BIN_PATH, str(index))


def get_binary_gz_path(index: int | str) -> str:
    return join(BIN_PATH, f"{index}.gz")


def get_patch_path(filename: str) -> str:
    return join(PATCHES_PATH, normpath(filename[5:]))


def get_json_raw_path(index: int | str) -> str:
    return join(JSON_RAW_PATH, f"{index}.json")


def get_json_patched_path(index: int | str) -> str:
    return join(JSON_PATCHED_PATH, f"{index}.json")


def get_directory_file_list(directory: str, sort_int: bool = False, pattern: str = "*") -> list[str]:
    files = glob(join(directory, pattern))
    if sort_int:
        ext = get_ext(files[0])
        # TODO
        # remove more one ext
        numbers = list(map(lambda file: rm_ext(basename(file)), files))
        numbers.sort(key=int)
        files = list(map(lambda file: join(
            directory, f"{file}{ext}"), numbers))
    else:
        files.sort()
    return files


def to_json_patched_path(path: str) -> str:
    return join(JSON_PATCHED_PATH, basename(path))


def remove_files(files: list[str]) -> None:
    for file in files:
        print(f"{Fore.RED}[Remove file]:{Style.RESET_ALL}", file)
        remove(file)


def rm_ext(path: str) -> str:
    return splitext(path)[0]


def add_ext(path: str, ext: str) -> str:
    return f"{path}{ext}"


def get_ext(path: str) -> str:
    return splitext(path)[1]


def get_index(path: str) -> int:
    return int(basename(splitext(path)[0]))
