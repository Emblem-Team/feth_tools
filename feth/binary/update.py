from feth.utils.path import (
    INFO0_PATH,
    get_patch_path,
    get_entry_binary_path,
    get_entry_binary_gz_path,
    copy_file,
)

from iostuff.readers.binary import BinaryReader
from colorama import Fore, Style

ENTRY_BLOCK_SIZE = 0x120


def update_binary() -> None:
    if not INFO0_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", INFO0_PATH)
        exit(1)

    info0_entry_count = INFO0_PATH.stat().st_size // ENTRY_BLOCK_SIZE

    with BinaryReader(INFO0_PATH) as reader:
        for _ in range(info0_entry_count):
            index = reader.read_ulong()
            decompressed_size = reader.read_ulong()
            compressed_size = reader.read_ulong()
            is_compressed = reader.read_ulong()
            filename = reader.read_utf8_nt_string()

            patch_path = get_patch_path(filename)

            if not patch_path.exists():
                print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", patch_path)
                continue

            if is_compressed:
                binary_gz_path = get_entry_binary_gz_path(index)
                print(
                    f"{Fore.GREEN}[Update binary gz]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_gz_path,
                )
                copy_file(patch_path, binary_gz_path)
            else:
                binary_path = get_entry_binary_path(index)
                print(
                    f"{Fore.GREEN}[Update binary]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_path,
                )
                copy_file(patch_path, binary_path)

            reader.align(ENTRY_BLOCK_SIZE)
