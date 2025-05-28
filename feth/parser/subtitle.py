from pathlib import Path
import shutil

from iostuff.readers.binary import BinaryReader


def parse_subtitle_files(dir_path: Path):
    dir_path = Path(dir_path)
    sub = Path("map")
    indexes = []
    for file_path in dir_path.glob("*"):
        if file_path.is_file():
            with BinaryReader(file_path) as reader:
                try:
                    magic = reader.read_uint()
                    count = reader.read_uint()
                    first_ofst = reader.read_uint()
                    if magic == 10594 and count * 4 + 8 == first_ofst:
                        # shutil.copyfile(
                        #     file_path, file_path.parent / map / file_path.stem
                        # )
                        indexes.append(int(file_path.stem))
                except Exception:
                    pass
    print(indexes)
