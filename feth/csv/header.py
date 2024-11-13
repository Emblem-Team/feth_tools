from __future__ import annotations


class NoneHeader:
    def __init__(self, none_index: int) -> None:
        self.none_index = none_index

    def __str__(self) -> str:
        return f"$NONE {self.none_index}"

    @staticmethod
    def from_row(row: list[str]) -> int:
        header = row[0]
        values = header.split(" ")
        return int(values[1])


class RepeatHeader:
    def __init__(self, repeat_index: int) -> None:
        self.repeat_index = repeat_index

    def __str__(self) -> str:
        return f"$REPEAT {self.repeat_index}"

    @staticmethod
    def from_row(row: list[str]) -> int:
        header = row[0]
        values = header.split(" ")
        return int(values[1])


class FileHeader:
    def __init__(
        self, file_index: int | str, file_type: str, entry_count: int = 0
    ) -> None:
        self.file_index = file_index
        self.file_type = file_type
        self.entry_count = entry_count

    def __str__(self) -> str:
        if self.entry_count != 0:
            return f"$FILE {self.file_index} $COUNT {self.entry_count} $TYPE {self.file_type}"
        else:
            return f"$FILE {self.file_index} $EMPTY $TYPE {self.file_type}"

    @staticmethod
    def from_row(row: list[str]) -> FileHeader:
        header = row[0]
        values = header.split(" ")

        if len(values) == 6:
            return FileHeader(values[1], values[5], int(values[3]))

        return FileHeader(values[1], values[4])
