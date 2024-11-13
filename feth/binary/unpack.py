from feth.utils.path import (
    get_entry_binary_path,
    get_entry_binary_gz_path,
    BIN_PATH,
    DATA0_PATH,
    DATA1_PATH,
)

from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter
from colorama import Fore, Style

ENTRY_BLOCK_SIZE = 0x20


def unpack_binary() -> None:
    if not DATA0_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", DATA0_PATH)
        exit(1)

    if not DATA1_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", DATA1_PATH)
        exit(1)

    if not BIN_PATH.exists():
        BIN_PATH.mkdir()

    data0_entry_count = DATA0_PATH.stat().st_size // ENTRY_BLOCK_SIZE
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
                    binary_gz_path = get_entry_binary_gz_path(index)
                    print(
                        f"{Fore.GREEN}[Unpack binary gz]:{Style.RESET_ALL}",
                        binary_gz_path,
                    )
                    with BinaryWriter(binary_gz_path) as writer:
                        data1_reader.seek(offset)
                        writer.write(data1_reader.read(compressed_size))
                else:
                    binary_path = get_entry_binary_path(index)
                    print(f"{Fore.GREEN}[Unpack binary]:{Style.RESET_ALL}", binary_path)
                    with BinaryWriter(binary_path) as writer:
                        data1_reader.seek(offset)
                        writer.write(data1_reader.read(decompressed_size))
