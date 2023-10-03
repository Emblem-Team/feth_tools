from app.utils.path import VARS_PATH

from iostuff.readers.csv import CSVReader

from re import findall

VARIABLE_REG = r"({{(.*?)}})"


class Variables:
    def __init__(self) -> None:
        self.variables = {}

    def load(self) -> None:
        with CSVReader(VARS_PATH) as reader:
            for row in reader:
                self.variables[row[0]] = row[1]

    def parse(self, line: str) -> str:
        expr = findall(VARIABLE_REG, line)
        if expr:
            for exp in expr:
                try:
                    line = line.replace(exp[0], self.variables[exp[1]])
                except KeyError:
                    continue
        return line
