from app.binary.gz import decompress_gz
from app.utils.path import (
    TUTORIALS_PATH,
    TUTORIALS_BIN_PATH,
    get_directory_file_list,
    rm_ext
)

from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter

from os.path import join, exists, basename
from os import makedirs


class BinaryArchiveModel:
    number_of_entries: int
    pointers: list[list[int]]
    entries: list[bytes]


def unpack_binary_archive(archive_path: str, output_path: str, entry_ext: str) -> None:
    if not exists(archive_path):
        print("[Not found]:", archive_path)
        exit(0)

    if not exists(output_path):
        makedirs(output_path)

    with BinaryReader(archive_path) as reader:
        file = BinaryArchiveModel()
        file.number_of_entries = reader.read_uint()

        file.pointers = []
        for _ in range(file.number_of_entries):
            file.pointers.append([reader.read_uint(), reader.read_uint()])

        file.entries = []
        for pointer in file.pointers:
            reader.seek(pointer[0])
            file.entries.append(reader.read(pointer[1]))

        for entry_idx, entry in enumerate(file.entries):
            entry_path = join(output_path, f"{entry_idx}.{entry_ext}")
            print("[Unpack binary archive data]:", entry_path)
            with BinaryWriter(entry_path) as writer:
                writer.write(entry)


def unpack_tutorials() -> None:
    if not exists(TUTORIALS_BIN_PATH):
        print("[Not found]:", TUTORIALS_BIN_PATH)
        exit(0)

    if not exists(TUTORIALS_PATH):
        makedirs(TUTORIALS_PATH)

    with BinaryReader(TUTORIALS_BIN_PATH) as reader:
        file = BinaryArchiveModel()
        file.number_of_entries = reader.read_uint()

        file.pointers = []
        for _ in range(file.number_of_entries):
            file.pointers.append([reader.read_uint(), reader.read_uint()])

        file.entries = []
        for pointer in file.pointers:
            reader.seek(pointer[0])
            file.entries.append(reader.read(pointer[1]))

        for entry_idx, entry in enumerate(file.entries):
            entry_path = join(TUTORIALS_PATH, f"{entry_idx}.g1t.gz")
            print("[Unpack tutorial]:", entry_path)
            with BinaryWriter(entry_path) as writer:
                writer.write(entry)


def decompress_tutorials() -> None:
    files = get_directory_file_list(TUTORIALS_PATH, True, "*.gz")
    for input_file in files:
        output_file = join(TUTORIALS_PATH, rm_ext(basename(input_file)))
        decompress_gz(input_file, output_file)
