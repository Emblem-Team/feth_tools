from app.utils.path import (
    get_directory_file_list,
    to_json_patched_path,
    JSON_RAW_PATH,
    BUNDLE_PATH,
    CSV_PATH,
    JSON_PATCHED_PATH,
    VARS_PATH
)
from app.utils.string import escape_str, scape_str
from app.csv.vars import Variables
from app.binary.compression.base import AbstractCompressionModel

from iostuff.readers.json import JsonReader
from iostuff.writers.json import JsonWriter
from iostuff.writers.csv import CSVWriter
from iostuff.readers.csv import CSVReader
import os


def make_bundle() -> None:
    if not os.path.exists(JSON_RAW_PATH):
        print("[Not found]:", JSON_RAW_PATH)
        exit(0)

    unique_strings = []
    file_list = get_directory_file_list(JSON_RAW_PATH, True)

    if not os.path.exists(CSV_PATH):
        os.makedirs(CSV_PATH)

    with CSVWriter(BUNDLE_PATH) as writer:
        for file_path in file_list:
            with JsonReader[AbstractCompressionModel](file_path) as model:
                strings = model.get_strings()
                for string in strings:
                    if string in unique_strings:
                        continue
                    if string == "":
                        continue
                    if not string:
                        continue
                    unique_strings.append(string)
                    writer.write_row([escape_str(string), ""])


def patch_bundle() -> None:
    if not os.path.exists(JSON_RAW_PATH):
        print("[Not found]:", JSON_RAW_PATH)
        exit(0)

    if not os.path.exists(BUNDLE_PATH):
        print("[Not found]:", BUNDLE_PATH)
        exit(0)

    if not os.path.exists(JSON_PATCHED_PATH):
        os.makedirs(JSON_PATCHED_PATH)

    file_list = get_directory_file_list(JSON_RAW_PATH, True)
    vars = None

    if os.path.exists(VARS_PATH):
        vars = Variables()
        vars.load()

    for file_path in file_list:
        patched_path = to_json_patched_path(file_path)
        with JsonReader[AbstractCompressionModel](file_path) as model:
            with JsonWriter[AbstractCompressionModel](patched_path) as writer:
                print("[Patch model]:", file_path, "->",
                      patched_path, f"({model.__class__.__name__})")
                with CSVReader(BUNDLE_PATH) as reader:
                    for row in reader:
                        raw, translated = row
                        if translated and translated != "":
                            if vars:
                                translated = vars.parse(translated)
                            model.apply_patch(
                                (scape_str(raw), scape_str(translated)))
                writer.write(model)
