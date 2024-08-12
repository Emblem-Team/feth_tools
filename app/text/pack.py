from app.utils.path import get_entry_mods_path, get_entry_json_patched_path, MODS_PATH
from app.binary.compression.base import (
    AbstractCompressionType,
    AbstractCompressionModel,
)
from app.binary.compression.support import SupportType
from app.binary.compression.map import MapType
from app.binary.compression.msgdata import MsgdataType
from app.binary.compression.subtitle import SubtitleType

from iostuff.readers.json import JsonReader
from iostuff.writers.binary import BinaryWriter

from os import makedirs
from os.path import exists
from colorama import Fore
from colorama import Style


def pack_type(type: AbstractCompressionType) -> None:
    if not exists(MODS_PATH):
        makedirs(MODS_PATH)

    for index in type.indexes:
        json_patched_path = get_entry_json_patched_path(index)
        mods_path = get_entry_mods_path(index)

        if not exists(json_patched_path):
            print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", json_patched_path)
            continue

        print(
            f"{Fore.GREEN}[Pack text]:{Style.RESET_ALL}",
            json_patched_path,
            "->",
            mods_path,
        )
        with JsonReader[AbstractCompressionModel](json_patched_path) as model:
            with BinaryWriter(mods_path) as writer:
                type.pack(model, writer)


def pack_text() -> None:
    pack_msgdata_text()
    pack_support_text()
    pack_map_text()
    pack_subtitle_text()


def pack_msgdata_text() -> None:
    pack_type(MsgdataType())


def pack_support_text() -> None:
    pack_type(SupportType())


def pack_map_text() -> None:
    pack_type(MapType())


def pack_subtitle_text() -> None:
    pack_type(SubtitleType())
