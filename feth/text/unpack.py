from feth.utils.path import (
    get_entry_binary_path,
    get_entry_json_raw_path,
    JSON_RAW_PATH,
)
from feth.binary.compression.base import AbstractCompressionType
from feth.binary.compression.support import SupportType
from feth.binary.compression.map import MapType
from feth.binary.compression.msgdata import MsgdataType
from feth.binary.compression.subtitle import SubtitleType

from iostuff.readers.binary import BinaryReader
from iostuff.writers.json import JsonWriter

from colorama import Fore, Style


def unpack_type(type: AbstractCompressionType) -> None:
    if not JSON_RAW_PATH.exists():
        JSON_RAW_PATH.mkdir(parents=True)

    for index in type.indexes:
        binary_path = get_entry_binary_path(index)
        json_raw_path = get_entry_json_raw_path(index)

        if not binary_path.exists():
            print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", binary_path)
            continue

        print(
            f"{Fore.GREEN}[Unpack text]:{Style.RESET_ALL}",
            binary_path,
            "->",
            json_raw_path,
            f"{Fore.CYAN}({type.__class__.__name__}){Style.RESET_ALL}",
        )
        with BinaryReader(binary_path) as reader:
            model = type.unpack(reader)
            with JsonWriter(json_raw_path) as writer:
                writer.write(model)


def unpack_text() -> None:
    unpack_msgdata_text()
    unpack_support_text()
    unpack_map_text()
    unpack_subtitle_text()


def unpack_support_text() -> None:
    unpack_type(SupportType())


def unpack_map_text() -> None:
    unpack_type(MapType())


def unpack_msgdata_text() -> None:
    unpack_type(MsgdataType())


def unpack_subtitle_text() -> None:
    unpack_type(SubtitleType())
