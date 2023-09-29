from os.path import join, normpath, basename, splitext
from os import listdir, remove

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
MODS_PATH = join(DATA_PATH, "mods")


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


def get_directory_file_list(directory: str, sort_int: bool = False) -> list[str]:
    names = listdir(directory)
    if sort_int:
        ext = get_ext(names[0])
        numbers = list(map(lambda name: rm_ext(name), names))
        numbers.sort(key=int)
        names = list(map(lambda number: add_ext(number, ext), numbers))
    else:
        names.sort()
    files = list(map(lambda file: join(
        directory, str(file)), names))
    return files


def to_json_patched_path(path: str) -> str:
    return join(JSON_PATCHED_PATH, basename(path))


def remove_files(files: list[str]) -> None:
    for file in files:
        print("[Remove file]:", file)
        remove(file)


def rm_ext(path: str) -> str:
    return splitext(path)[0]


def add_ext(path: str, ext: str) -> str:
    return f"{path}{ext}"


def get_ext(path: str) -> str:
    return splitext(path)[1]
