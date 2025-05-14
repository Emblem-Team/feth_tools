from feth.utils.path import VARS_PATH
from iostuff.readers.csv import CSVReader


class Variables:
    def __init__(self) -> None:
        self.variables = []

    def load(self) -> None:
        with CSVReader(VARS_PATH) as reader:
            for row in reader:
                self.variables.append(row)
        self.variables = sorted(self.variables, key=lambda x: (-len(x[0]), x[0]))

    def parse(self, line: str) -> str:
        for v in self.variables:
            line = line.replace(v[0], v[1])
        return line
