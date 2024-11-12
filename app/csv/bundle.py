from pathlib import Path
from app.utils.path import (
    get_entry_json_raw_path,
    to_csv_path,
    to_json_patched_path,
    JSON_RAW_PATH,
    BUNDLE_PATH,
    CSV_PATH,
    JSON_PATCHED_PATH,
    VARS_PATH,
)
from app.utils.string import escape_str, scape_str
from app.csv.vars import Variables
from app.binary.compression.base import AbstractCompressionModel
from app.csv.header import FileHeader, NoneHeader, RepeatHeader
from iostuff.readers.json import JsonReader
from iostuff.writers.json import JsonWriter
from iostuff.writers.csv import CSVWriter
from iostuff.readers.csv import CSVReader
from colorama import Fore, Style
import json


def make_bundle() -> None:
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not CSV_PATH.exists():
        CSV_PATH.mkdir(parents=True)

    with CSVWriter(BUNDLE_PATH) as writer:
        # define global flags
        buf = None
        repeat_index = 0
        repeat_before = False
        none_index = 0
        none_before = False

        for json_path in JSON_RAW_PATH.glob("*.json"):
            with JsonReader[AbstractCompressionModel](json_path) as model:
                file_index = json_path.stem
                file_type = model.str()
                entry_count = len(model.strings)

                # if file is empty, define empty header and continue loop
                if entry_count == 1 and model.strings[0] == "":
                    writer.write_row([FileHeader(file_index, file_type), ""])
                    continue

                # if not, define normal header with entry count
                writer.write_row([FileHeader(file_index, file_type, entry_count), ""])

                for string in model.strings:
                    # if entry is empty, then increase none index and continue loop
                    if string == "" or not string:
                        none_index += 1
                        none_before = True
                        continue

                    # if entry eq buf, then increase repeat index and continue loop
                    if string == buf:
                        repeat_index += 1
                        repeat_before = True
                        continue

                    # if entry repeat before, define repeat header and disable flags
                    if repeat_before:
                        writer.write_row([RepeatHeader(repeat_index), ""])
                        repeat_index = 0
                        repeat_before = False

                    # if entry none before, define none header and disable flags
                    if none_before:
                        writer.write_row([NoneHeader(none_index), ""])
                        none_index = 0
                        none_before = False

                    # buf eq entry
                    buf = string

                    # write entry
                    writer.write_row([escape_str(string), ""])

                # if entry repeat before, define repeat header and disable flags
                if repeat_before:
                    writer.write_row([RepeatHeader(repeat_index), ""])
                    repeat_index = 0
                    repeat_before = False

                # if entry none before, define none header and disable flags
                if none_before:
                    writer.write_row([NoneHeader(none_index), ""])
                    none_index = 0
                    none_before = False


def patch_bundle() -> None:
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not BUNDLE_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", BUNDLE_PATH)
        exit(0)

    if not JSON_PATCHED_PATH.exists():
        JSON_PATCHED_PATH.mkdir(parents=True)

    with CSVReader(BUNDLE_PATH) as csv_reader:
        # define global flags
        file_header = None
        buf = None
        repeat_index = 0
        none_index = 0
        model = None
        writer = None
        strings = []

        for row in csv_reader:
            # if row is file header, parse header and initialize file
            if row[0].startswith("$FILE"):
                if writer:
                    print(file_header.file_index, len(strings), len(model.strings))
                    model.patch(strings)
                    writer.write(model)
                    writer.close()
                    strings = []
                    buf = None
                if "$EMPTY" in row[0]:
                    continue
                file_header = FileHeader.from_row(row)
                file_path = get_entry_json_raw_path(file_header.file_index)
                patched_path = to_json_patched_path(file_path)
                model = JsonReader[AbstractCompressionModel](file_path).open()
                writer = JsonWriter[AbstractCompressionModel](patched_path).open()
                continue

            # if row is none header, parse header and write null entries
            if row[0].startswith("$NONE"):
                none_index = NoneHeader.from_row(row)
                for _ in range(none_index):
                    strings.append("")
                continue

            # if row is repeat header, parse header and write repeat buf entry
            if row[0].startswith("$REPEAT"):
                repeat_index = RepeatHeader.from_row(row)
                for _ in range(repeat_index):
                    strings.append(buf)
                continue

            if row[1] == "":
                strings.append(scape_str(row[0]))
                buf = row[0]
            else:
                strings.append(scape_str(row[1]))
                buf = row[1]
