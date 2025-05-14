from feth.utils.path import get_entry_mods_path, get_entry_json_patched_path, MODS_PATH
from feth.binary.compression.base import (
    AbstractCompressionType,
    AbstractCompressionModel,
)
from feth.binary.compression.support import SupportType
from feth.binary.compression.map import MapType
from feth.binary.compression.msgdata import MsgdataType
from feth.binary.compression.subtitle import SubtitleType

from iostuff.readers.json import JsonReader
from iostuff.writers.binary import BinaryWriter

from colorama import Fore, Style


def pack_type(type: AbstractCompressionType) -> None:
    if not MODS_PATH.exists():
        MODS_PATH.mkdir(parents=True)

    for index in type.indexes:
        json_patched_path = get_entry_json_patched_path(index)
        mods_path = get_entry_mods_path(index)

        if not json_patched_path.exists():
            print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", json_patched_path)
            continue

        print(
            f"{Fore.GREEN}[Pack text]:{Style.RESET_ALL}",
            json_patched_path.name,
            "->",
            mods_path.name,
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
