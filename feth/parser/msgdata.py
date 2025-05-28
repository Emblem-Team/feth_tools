from pathlib import Path
import shutil

from iostuff.readers.binary import BinaryReader


def parse_msgdata_files(dir_path: Path):
    dir_path = Path(dir_path)
    msgdata = Path("msgdata")
    indexes = []
    for file_path in dir_path.glob("*"):
        if file_path.is_file():
            with BinaryReader(file_path) as reader:
                try:
                    count = reader.read_uint()
                    first_ofst = reader.read_uint()
                    if count == 12 and count * 8 + 4 == first_ofst:
                        # shutil.copyfile(
                        #     file_path, file_path.parent / msgdata / file_path.stem
                        # )
                        indexes.append(int(file_path.stem))
                except Exception:
                    pass
    print(indexes)
