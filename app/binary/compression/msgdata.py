from app.common.indexes import MSGDATA_TEXT_INDEXES
from app.utils.enums import LanguageEnum
from app.utils.common import actived_flags_count
from app.binary.compression.base import (
    AbstractCompressionType,
    AbstractCompressionModel,
)

from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter
from iostuff.common.utf8 import utf8_string_length


class Table:
    magic: int
    table_size: int
    flag_size: int
    number_of_pointers: int
    pointer_size: int
    header_size: int
    flags: list[int]
    pointers: list[list[int]]
    text: list[list[str]]


class Language:
    number_of_tables: int
    pointers: list[list[int]]
    tables: list[Table]


class MsgdataModel(AbstractCompressionModel):
    number_of_languages: int
    pointers: list[list[int]]
    languages: list[Language]

    @property
    def strings(self) -> list[str]:
        strings = []
        for table in self.languages[LanguageEnum.ENG_E].tables:
            for text in table.text:
                for line in text:
                    strings.append(line)
        return strings

    def patch(self, strings: list[str]) -> None:
        string_idx = 0
        for table in self.languages[LanguageEnum.ENG_E].tables:
            for text in table.text:
                for line_index, _ in enumerate(text):
                    text[line_index] = strings[string_idx]
                    string_idx += 1

    def str(self) -> str:
        return "MSGDATA"


class MsgdataType(AbstractCompressionType):
    def __init__(self) -> None:
        self.indexes = MSGDATA_TEXT_INDEXES

    def unpack(self, reader: BinaryReader) -> MsgdataModel:
        file = MsgdataModel()
        file.number_of_languages = reader.read_uint()

        file.pointers = []
        for _ in range(file.number_of_languages):
            file.pointers.append([reader.read_uint(), reader.read_uint()])

        file.languages = []
        for _ in range(file.number_of_languages):
            language = Language()

            language.number_of_tables = reader.read_uint()

            language.pointers = []
            for _ in range(language.number_of_tables):
                language.pointers.append([reader.read_uint(), reader.read_uint()])

            language.tables = []
            for _ in range(language.number_of_tables):
                table = Table()

                table.magic = reader.read_uint()
                table.table_size = reader.read_ushort()
                table.flag_size = reader.read_ushort()
                table.number_of_pointers = reader.read_ushort()
                table.pointer_size = reader.read_ushort()
                table.header_size = reader.read_uint()

                table.flags = []
                for _ in range(table.flag_size):
                    table.flags.append(reader.read_ubyte())

                reader.align(4)

                table.pointers = []
                for _ in range(table.number_of_pointers):
                    pointer = []
                    for _ in range(table.flag_size):
                        pointer.append(reader.read_uint())
                    table.pointers.append(pointer)

                table.text = []
                for _ in range(table.number_of_pointers):
                    actived_flags = actived_flags_count(table.flags)
                    if actived_flags == 0:
                        break
                    entry = []
                    for _ in range(actived_flags):
                        entry.append(reader.read_utf8_nt_string())
                    table.text.append(entry)

                reader.align(4)

                language.tables.append(table)
            file.languages.append(language)

        return file

    def pack(self, model: MsgdataModel, writer: BinaryWriter) -> None:
        self.calculate_language_pointers(model)
        for language in model.languages:
            self.calculate_table_pointers(language)
            for table in language.tables:
                self.calculate_text_pointers(table)

        writer.write_uint(model.number_of_languages)

        for pointer in model.pointers:
            writer.write_uint(pointer[0])
            writer.write_uint(pointer[1])

        for language in model.languages:
            writer.write_uint(language.number_of_tables)

            for pointer in language.pointers:
                writer.write_uint(pointer[0])
                writer.write_uint(pointer[1])

            for table in language.tables:
                writer.write_uint(table.magic)
                writer.write_ushort(table.table_size)
                writer.write_ushort(table.flag_size)
                writer.write_ushort(table.number_of_pointers)
                writer.write_ushort(table.pointer_size)
                writer.write_uint(table.header_size)

                for flag in table.flags:
                    writer.write_ubyte(flag)

                for pointer_entry in table.pointers:
                    for pointer in pointer_entry:
                        writer.write_uint(pointer)

                for entry in table.text:
                    for line in entry:
                        writer.write_utf8_nt_string(line)

    def calculate_text_size(self, text: list[list[str]]) -> int:
        size = 0
        for entry in text:
            for line in entry:
                size += utf8_string_length(line) + 1  # zero byte
        return size

    def calculate_table_size(self, table: Table) -> int:
        header_size = 16 + table.flag_size
        pointers_size = table.number_of_pointers * table.pointer_size
        text_size = self.calculate_text_size(table.text)
        table.header_size = header_size
        return header_size + pointers_size + text_size

    def calculate_language_size(self, lang: Language) -> int:
        header_size = 4
        pointers_size = lang.number_of_tables * 8
        tables_size = 0

        for table in lang.tables:
            tables_size += self.calculate_table_size(table)

        return header_size + pointers_size + tables_size

    def calculate_language_pointers(self, file: MsgdataModel) -> None:
        header_size = 4
        pointers_size = file.number_of_languages * 8
        relative_offset = header_size + pointers_size
        file.pointers = []

        for language in file.languages:
            offset = relative_offset
            size = self.calculate_language_size(language)
            file.pointers.append([offset, size])
            relative_offset += size

    def calculate_table_pointers(self, language: Language) -> None:
        header_size = 4
        pointers_size = language.number_of_tables * 8
        relative_offset = header_size + pointers_size
        language.pointers = []

        for table in language.tables:
            offset = relative_offset
            size = self.calculate_table_size(table)
            language.pointers.append([offset, size])
            relative_offset += size

    def calculate_text_pointers(self, table: Table) -> None:
        relative_offset = table.pointer_size * table.number_of_pointers
        for entry_index, entry in enumerate(table.text):
            for line_index, line in enumerate(entry):
                table.pointers[entry_index][line_index] = relative_offset
                relative_offset += utf8_string_length(line) + 1
