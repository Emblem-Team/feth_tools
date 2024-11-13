from feth.common.indexes import MAP_TEXT_INDEXES
from feth.binary.compression.base import (
    AbstractCompressionModel,
    AbstractCompressionType,
)

from iostuff.common.utf8 import utf8_string_length
from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter


class MapModel(AbstractCompressionModel):
    number_of_pointers: int
    pointers: list[list[int]]
    text: list[str]

    @property
    def strings(self) -> list[str]:
        return self.text

    def patch(self, strings: list[str]) -> None:
        string_idx = 0
        for line_index, _ in enumerate(self.text):
            self.text[line_index] = strings[string_idx]
            string_idx += 1

    def str(self) -> str:
        return "MAP"


class MapType(AbstractCompressionType):
    def __init__(self) -> None:
        self.indexes = MAP_TEXT_INDEXES

    def unpack(self, reader: BinaryReader) -> MapModel:
        file = MapModel()
        file.number_of_pointers = reader.read_uint()

        file.pointers = []
        for _ in range(file.number_of_pointers):
            file.pointers.append([reader.read_uint(), reader.read_uint()])

        file.text = []
        for _ in range(file.number_of_pointers):
            file.text.append(reader.read_utf8_nt_string())

        return file

    def pack(self, model: MapModel, writer: BinaryWriter) -> None:
        writer.write_uint(len(model.text))

        pointers: list[list[int]] = self.calculate_pointers(model.text)
        for pointer in pointers:
            writer.write_uint(pointer[0])
            writer.write_uint(pointer[1])

        for i in range(len(model.text)):
            writer.write_utf8_nt_string(model.text[i])

    def calculate_pointers(self, text: list[str]) -> list[list[int]]:
        header_size = 4
        pointers_size = 8 * len(text)
        relative_offset = header_size + pointers_size
        pointers = []
        for line in text:
            offset = relative_offset
            size = utf8_string_length(line) + 1  # zero byte
            pointers.append([offset, size])
            relative_offset += size
        return pointers
