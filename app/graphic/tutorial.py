from app.binary.gz import decompress_gz
from app.utils.path import TUTORIALS_PATH, TUTORIALS_BIN_PATH
from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter
from pathlib import Path


class BinaryArchiveModel:
    number_of_entries: int
    pointers: list[list[int]]
    entries: list[bytes]


def unpack_binary_archive(
    archive_path: Path, output_path: Path, entry_ext: str
) -> None:
    if not archive_path.exists():
        print("[Not found]:", archive_path)
        exit(1)

    if not output_path.exists():
        output_path.mkdir()

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
            entry_path = output_path / f"{entry_idx}.{entry_ext}"
            print("[Unpack binary archive data]:", entry_path)
            with BinaryWriter(entry_path) as writer:
                writer.write(entry)


def unpack_tutorials() -> None:
    if not TUTORIALS_BIN_PATH.exists():
        print("[Not found]:", TUTORIALS_BIN_PATH)
        exit(1)

    if not TUTORIALS_PATH.mkdir():
        TUTORIALS_PATH.mkdir()

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
            entry_path = TUTORIALS_PATH / f"{entry_idx}.g1t.gz"
            print("[Unpack tutorial]:", entry_path)
            with BinaryWriter(entry_path) as writer:
                writer.write(entry)


def decompress_tutorials() -> None:
    for input_file in TUTORIALS_PATH.glob("*.gz"):
        output_file = TUTORIALS_PATH / input_file.stem
        decompress_gz(input_file, output_file)
