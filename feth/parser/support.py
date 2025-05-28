from pathlib import Path
import shutil

from iostuff.readers.binary import BinaryReader


def parse_support_files(dir_path: Path):
    dir_path = Path(dir_path)
    sup = Path("support")
    indexes = []
    for file_path in dir_path.glob("*"):
        if file_path.is_file():
            with BinaryReader(file_path) as reader:
                try:
                    if (
                        reader.read_uint() == 1
                        and reader.read_uint() == 1
                        and reader.read_uint() == 32
                    ):
                        # shutil.copyfile(
                        #     file_path, file_path.parent / sup / file_path.stem
                        # )
                        indexes.append(int(file_path.stem))
                except Exception:
                    pass
    print(indexes)
