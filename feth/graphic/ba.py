from pathlib import Path

from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter


class BinaryArchiveModel:
    number_of_entries: int
    pointers: list[list[int]]
    entries: list[bytes]


def unpack_binary_archive(
    archive_path: Path, output_path: Path, entry_ext: str
) -> None:
    archive_path = Path(archive_path)
    output_path = Path(output_path)
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
