from feth.common.indexes import CREDIT_INDEXES
from feth.binary.compression.base import (
    AbstractCompressionModel,
    AbstractCompressionType,
)

from iostuff.common.utf8 import utf8_string_length
from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter


class CreditModel(AbstractCompressionModel):
    magic: int
    number_of_pointers: int
    pointers: list[int]
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
        return "CREDIT"


class CreditType(AbstractCompressionType):
    def __init__(self) -> None:
        self.indexes = [*CREDIT_INDEXES]

    def unpack(self, reader: BinaryReader) -> CreditModel:
        file = CreditModel()
        file.magic = reader.read_uint()
        file.number_of_pointers = reader.read_uint()

        file.pointers = []
        for _ in range(file.number_of_pointers):
            file.pointers.append(reader.read_uint())

        file.text = []
        for i in range(file.number_of_pointers):
            reader.seek(file.pointers[i])
            if i == file.number_of_pointers - 1:
                file.text.append("\0")
                continue
            size = file.pointers[i+1] - file.pointers[i]
            file.text.append(reader.read_utf8_string(size))

        return file

    def pack(self, model: CreditModel, writer: BinaryWriter) -> None:
        writer.write_uint(model.magic)
        writer.write_uint(len(model.text))

        pointers: list[int] = self.calculate_pointers(model.text)
        for pointer in pointers:
            writer.write_uint(pointer)

        for i in range(len(model.text)):
            writer.write_utf8_string(model.text[i])

    def calculate_pointers(self, text: list[str]) -> list[int]:
        header_size = 8
        pointers_size = 4 * len(text)
        relative_offset = header_size + pointers_size
        pointers = []
        for line in text:
            offset = relative_offset
            size = utf8_string_length(line)
            pointers.append(offset)
            relative_offset += size
        return pointers
