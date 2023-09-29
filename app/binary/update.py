from app.utils.path import (
    INFO0_PATH,
    get_patch_path,
    get_binary_path,
    get_binary_gz_path
)
from iostuff.readers.binary import BinaryReader
from os.path import getsize, exists
from shutil import copyfile


def update_binary() -> None:
    if not exists(INFO0_PATH):
        print("[Not found]:", INFO0_PATH)
        exit(1)

    info0_entry_count = getsize(INFO0_PATH) // 0x120

    with BinaryReader(INFO0_PATH) as reader:
        for _ in range(info0_entry_count):
            index = reader.read_ulong()
            decompressed_size = reader.read_ulong()
            compressed_size = reader.read_ulong()
            is_compressed = reader.read_ulong()
            filename = reader.read_utf8_nt_string()

            patch_path = get_patch_path(filename)

            if not exists(patch_path):
                print("[Not found]:", patch_path)
                continue

            if is_compressed:
                binary_gz_path = get_binary_gz_path(index)
                print("[Update binary gz]:", patch_path, "->", binary_gz_path)
                copyfile(patch_path, binary_gz_path)
            else:
                binary_path = get_binary_path(index)
                print("[Update binary]:", patch_path, "->", binary_path)
                copyfile(patch_path, binary_path)

            reader.align(0x120)
