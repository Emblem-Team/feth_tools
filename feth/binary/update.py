from feth.utils.path import (
    INFO0_PATH,
    INFO1_PATH,
    get_patch_path,
    get_entry_binary_path,
    get_entry_binary_gz_path,
    copy_file,
)

from iostuff.readers.binary import BinaryReader
from colorama import Fore, Style

INFO0_ENTRY_BLOCK_SIZE = 0x120
INFO1_ENTRY_BLOCK_SIZE = 0x118

BASE_DATA_ENTRY_COUNT = 31160


def update_info0_binary() -> None:
    if not INFO0_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", INFO0_PATH)
        exit(1)

    info0_entry_count = INFO0_PATH.stat().st_size // INFO0_ENTRY_BLOCK_SIZE

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
                    f"{Fore.GREEN}[Update info0 binary gz]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_gz_path,
                )
                copy_file(patch_path, binary_gz_path)
            else:
                binary_path = get_entry_binary_path(index)
                print(
                    f"{Fore.GREEN}[Update info0 binary]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_path,
                )
                copy_file(patch_path, binary_path)

            reader.align(INFO0_ENTRY_BLOCK_SIZE)


def update_info1_binary() -> None:
    if not INFO1_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", INFO1_PATH)
        exit(1)

    info1_entry_count = INFO1_PATH.stat().st_size // INFO1_ENTRY_BLOCK_SIZE

    with BinaryReader(INFO1_PATH) as reader:
        for index in range(
            BASE_DATA_ENTRY_COUNT, BASE_DATA_ENTRY_COUNT + info1_entry_count
        ):
            decompressed_size = reader.read_ulong()
            compressed_size = reader.read_ulong()
            is_compressed = reader.read_ulong()
            filename = reader.read_utf8_nt_string()

            patch_path = get_patch_path(filename)

            if not patch_path.exists():
                print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", patch_path)
                binary_path = get_entry_binary_path(index)
                binary_path.write_bytes(b"")
                reader.align(INFO1_ENTRY_BLOCK_SIZE)
                continue

            if is_compressed:
                binary_gz_path = get_entry_binary_gz_path(index)
                print(
                    f"{Fore.GREEN}[Update info1 binary gz]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_gz_path,
                )
                copy_file(patch_path, binary_gz_path)
            else:
                binary_path = get_entry_binary_path(index)
                print(
                    f"{Fore.GREEN}[Update info1 binary]:{Style.RESET_ALL}",
                    patch_path,
                    "->",
                    binary_path,
                )
                copy_file(patch_path, binary_path)

            reader.align(INFO1_ENTRY_BLOCK_SIZE)
