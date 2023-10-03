from app.common.indexes import SUBTITLE_TEXT_INDEXES
from app.binary.compression.base import (
    AbstractCompressionModel,
    AbstractCompressionType
)

from iostuff.common.utf8 import utf8_string_length
from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter


class SubtitleModel(AbstractCompressionModel):
    magic: int
    count: int
    offsets: list[int]
    lines: list[list]

    def get_strings(self) -> list[str]:
        return list(map(lambda line: line[1], self.lines))

    def apply_patch(self, patch: tuple[str, str]) -> None:
        for line_index, line in enumerate(self.lines):
            if line[1] == patch[0]:
                self.lines[line_index][1] = patch[1]

    def apply_fix(self, fix: list) -> None:
        self.lines[int(fix[1])][1] = fix[4]


class SubtitleType(AbstractCompressionType):
    def __init__(self) -> None:
        self.indexes = SUBTITLE_TEXT_INDEXES

    def unpack(self, reader: BinaryReader) -> SubtitleModel:
        model = SubtitleModel()
        model.magic = reader.read_uint()
        model.count = reader.read_uint()
        model.offsets = []
        model.lines = []

        for _ in range(model.count):
            model.offsets.append(reader.read_uint())

        for i in range(model.count):
            reader.seek(model.offsets[i])
            unk = reader.read_ulong()
            line = reader.read_utf8_nt_string()
            model.lines.append([unk, line])

        return model

    def pack(self, model: SubtitleModel, writer: BinaryWriter) -> None:
        writer.write_uint(model.magic)
        writer.write_uint(model.count)

        for offset in self.calculate_offsets(model):
            writer.write_uint(offset)

        for line in model.lines:
            writer.write_ulong(line[0])
            writer.write_utf8_nt_string(line[1])

    def calculate_offsets(self, model: SubtitleModel) -> list[int]:
        relative_offset = model.count * 4 + 8
        offsets = [relative_offset]

        for i in range(model.count - 1):
            size = utf8_string_length(model.lines[i][1]) + 8 + 1
            offsets.append(relative_offset + size)
            relative_offset += size

        return offsets
