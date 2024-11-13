from feth.utils.path import FIXES_PATH

from iostuff.readers.csv import CSVReader


class Fixes:
    def __init__(self) -> None:
        self.items = []

    def load(self) -> None:
        with CSVReader(FIXES_PATH) as reader:
            for row in reader:
                self.items.append(row)
