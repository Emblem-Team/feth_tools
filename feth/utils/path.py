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

INFO0_PATH = PATCHES_PATH / "patch4" / "INFO0.bin"

JSON_RAW_PATH = JSON_PATH / "raw"
JSON_PATCHED_PATH = JSON_PATH / "patched"

BUNDLE_PATH = CSV_PATH / "bundle.csv"
VARS_PATH = CSV_PATH / "vars.csv"

TUTORIALS_PATH = GRAPHIC_PATH / "tutorials"


def get_entry_mods_path(entry_index: int | str) -> Path:
    return MODS_PATH / str(entry_index)


def get_entry_binary_path(entry_index: int | str) -> Path:
    return BIN_PATH / str(entry_index)


def get_entry_binary_gz_path(entry_index: int | str) -> Path:
    return BIN_PATH / f"{entry_index}.gz"


def get_patch_path(filename: str) -> Path:
    return PATCHES_PATH / Path(filename[5:])


def get_entry_json_raw_path(entry_index: int | str) -> Path:
    return JSON_RAW_PATH / f"{entry_index}.json"


def get_entry_json_patched_path(entry_index: int | str) -> Path:
    return JSON_PATCHED_PATH / f"{entry_index}.json"


def copy_file(src: Path, dst: Path) -> int:
    return dst.write_bytes(src.read_bytes())


def to_json_patched_path(path: Path) -> Path:
    return JSON_PATCHED_PATH / path.name


def to_csv_path(path: Path) -> Path:
    return CSV_PATH / f"{path.stem}.csv"
