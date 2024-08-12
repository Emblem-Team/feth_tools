from os import remove
from os.path import join, normpath, basename, splitext
from colorama import Fore
from colorama import Style
from glob import glob
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = Path(getenv("DATA"))
PATCHES_PATH = Path(getenv("PATCHES"))

DATA0_PATH = Path(getenv("DATA0"))
DATA1_PATH = Path(getenv("DATA1"))

BIN_PATH = DATA_PATH / "bin"
JSON_PATH = DATA_PATH / "json"
CSV_PATH = DATA_PATH / "csv"
MODS_PATH = DATA_PATH / "mods"
GRAPHIC_PATH = DATA_PATH / "graphic"

TUTORIALS_BIN_PATH = BIN_PATH / "6131"

INFO0_PATH = PATCHES_PATH / "INFO0.bin"

JSON_RAW_PATH = JSON_PATH / "raw"
JSON_PATCHED_PATH = JSON_PATH / "patched"

BUNDLE_PATH = CSV_PATH / "bundle.csv"
VARS_PATH = CSV_PATH / "vars.csv"
FIXES_PATH = CSV_PATH / "fixes.csv"

TUTORIALS_PATH = GRAPHIC_PATH / "tutorials"


def get_entry_mods_path(entry_index: int | str) -> Path:
    return MODS_PATH / str(entry_index)


def get_entry_binary_path(entry_index: int | str) -> Path:
    return BIN_PATH / str(entry_index)


def get_entry_binary_gz_path(entry_index: int | str) -> Path:
    return BIN_PATH / f"{entry_index}.gz"


def get_patch_path(filename: str) -> Path:
    return PATCHES_PATH / normpath(filename[5:])


def get_entry_json_raw_path(entry_index: int | str) -> Path:
    return JSON_RAW_PATH / f"{entry_index}.json"


def get_entry_json_patched_path(entry_index: int | str) -> Path:
    return JSON_PATCHED_PATH / f"{entry_index}.json"


def get_directory_file_list(
    directory: str, sort_int: bool = False, pattern: str = "*"
) -> list[str]:
    files = glob(join(directory, pattern))
    if sort_int:
        ext = get_ext(files[0])
        # TODO
        # remove more one ext
        numbers = list(map(lambda file: rm_ext(basename(file)), files))
        numbers.sort(key=int)
        files = list(map(lambda file: join(directory, f"{file}{ext}"), numbers))
    else:
        files.sort()
    return files


def to_json_patched_path(path: Path) -> Path:
    return JSON_PATCHED_PATH / path.name


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


def get_index(path: Path) -> int:
    return int(path.stem)
