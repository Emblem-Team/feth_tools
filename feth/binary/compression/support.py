from feth.common.indexes import SUPPORT_TEXT_INDEXES, DLC_SUPPORT_INDEXES
from feth.binary.compression.base import (
    AbstractCompressionType,
    AbstractCompressionModel,
)

from iostuff.common.utf8 import utf8_string_length
from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter


class SupportModel(AbstractCompressionModel):
    unk: int
    pointer_table_offset: int
    pointer_table_size: int
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
        return "SUPPORT"


class SupportType(AbstractCompressionType):
    def __init__(self) -> None:
        self.indexes = [*SUPPORT_TEXT_INDEXES, *DLC_SUPPORT_INDEXES]

    def unpack(self, reader: BinaryReader) -> SupportModel:
        file = SupportModel()
        file.unk = reader.read_ulong()
        file.pointer_table_offset = reader.read_uint()
        file.pointer_table_size = reader.read_uint()
        file.number_of_pointers = reader.read_uint()

        reader.seek(file.pointer_table_offset)

        file.pointers = []
        for _ in range(file.number_of_pointers + 1):
            file.pointers.append(reader.read_uint())

        text_relative_offset = file.pointer_table_offset + file.pointer_table_size

        file.text = []
        for i in range(file.number_of_pointers):
            reader.seek(text_relative_offset + file.pointers[i])
            file.text.append(reader.read_utf8_nt_string())

        return file

    def pack(self, model: SupportModel, writer: BinaryWriter) -> None:
        writer.write_ulong(model.unk)
        writer.write_uint(32)
        writer.write_uint(0)  # zero offset
        writer.write_uint(len(model.text))

        writer.align(16)

        pointers: list[int] = self.calculate_pointers(model.text)
        for pointer in pointers:
            writer.write_uint(pointer)
        
        writer.align(16)

        temp = writer.tell()
        writer.seek(0xC)
        writer.write_uint(temp - 32)
        writer.seek(temp)

        for i in range(len(model.text)):
            writer.write_utf8_nt_string(model.text[i])

    def calculate_pointers(self, text: list[str]) -> list[int]:
        relative_offset = 0
        pointers = [relative_offset]

        for line in text:
            size = utf8_string_length(line) + 1  # zero byte
            pointers.append(relative_offset + size)
            relative_offset += size

        return pointers
