from app.utils.path import get_binary_path, get_json_raw_path, JSON_RAW_PATH
from app.binary.compression.base import AbstractCompressionType
from app.binary.compression.support import SupportType
from app.binary.compression.map import MapType
from app.binary.compression.msgdata import MsgdataType
from app.binary.compression.subtitle import SubtitleType

from iostuff.readers.binary import BinaryReader
from iostuff.writers.json import JsonWriter

import os


def unpack_type(type: AbstractCompressionType) -> None:
    if not os.path.exists(JSON_RAW_PATH):
        os.makedirs(JSON_RAW_PATH)

    for index in type.indexes:
        binary_path = get_binary_path(index)
        json_raw_path = get_json_raw_path(index)

        if not os.path.exists(binary_path):
            print("[Not found]:", binary_path)
            continue

        print("[Unpack text]:", binary_path, "->",
              json_raw_path, f"({type.__class__.__name__})")
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
