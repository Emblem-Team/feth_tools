from app.utils.path import (
    get_binary_path,
    get_binary_gz_path,
    BIN_PATH,
    DATA0_PATH,
    DATA1_PATH
)

from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter

from os import makedirs
from os.path import exists, getsize


def unpack_binary() -> None:
    if not exists(DATA0_PATH):
        print("[Not found]:", DATA0_PATH)
        exit(1)

    if not exists(DATA1_PATH):
        print("[Not found]:", DATA1_PATH)
        exit(1)

    if not exists(BIN_PATH):
        makedirs(BIN_PATH)

    data0_entry_count = getsize(DATA0_PATH) // 0x20
    with BinaryReader(DATA0_PATH) as data0_reader:
        with BinaryReader(DATA1_PATH) as data1_reader:
            for index in range(data0_entry_count):
                offset = data0_reader.read_ulong()
                decompressed_size = data0_reader.read_ulong()
                compressed_size = data0_reader.read_ulong()
                is_compressed = data0_reader.read_ulong()

                if decompressed_size == 0 and compressed_size == 0:
                    continue

                if is_compressed:
                    binary_gz_path = get_binary_gz_path(index)
                    print("[Unpack binary gz]:", binary_gz_path)
                    with BinaryWriter(binary_gz_path) as writer:
                        data1_reader.seek(offset)
                        writer.write(data1_reader.read(compressed_size))
                else:
                    binary_path = get_binary_path(index)
                    print("[Unpack binary]:", binary_path)
                    with BinaryWriter(binary_path) as writer:
                        data1_reader.seek(offset)
                        writer.write(data1_reader.read(decompressed_size))
