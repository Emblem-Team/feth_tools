from feth.utils.path import (
    to_json_patched_path,
    JSON_RAW_PATH,
    BUNDLE_PATH,
    DLC_BUNDLE_PATH,
    CSV_PATH,
    JSON_PATCHED_PATH,
    gen_json_path,
)
from feth.common.indexes import DLC_INDEXES, BASE_INDEXES
from feth.utils.string import escape_str, scape_str
from feth.binary.compression.base import AbstractCompressionModel
from iostuff.readers.json import JsonReader
from iostuff.writers.json import JsonWriter
from iostuff.writers.csv import CSVWriter
from iostuff.readers.csv import CSVReader
from colorama import Fore, Style


def make_bundle() -> None:
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not CSV_PATH.exists():
        CSV_PATH.mkdir(parents=True)

    with CSVWriter(BUNDLE_PATH) as writer:
        writer.write_row(
            ["file_index", "file_type", "source_language", "destination_language"]
        )
        for json_path in gen_json_path(BASE_INDEXES):
            with JsonReader[AbstractCompressionModel](json_path) as model:
                file_index = json_path.stem
                file_type = model.str()
                for string in model.strings:
                    if string == "" or string == None:
                        writer.write_row([file_index, file_type, "$NONE", "$NONE"])
                    else:
                        writer.write_row(
                            [file_index, file_type, escape_str(string), ""]
                        )


def make_dlc_bundle() -> None:
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not CSV_PATH.exists():
        CSV_PATH.mkdir(parents=True)

    with CSVWriter(DLC_BUNDLE_PATH) as writer:
        writer.write_row(
            ["file_index", "file_type", "source_language", "destination_language"]
        )
        for json_path in gen_json_path(DLC_INDEXES):
            with JsonReader[AbstractCompressionModel](json_path) as model:
                file_index = json_path.stem
                file_type = model.str()
                for string in model.strings:
                    if string == "" or string == None:
                        writer.write_row([file_index, file_type, "$NONE", "$NONE"])
                    else:
                        writer.write_row(
                            [file_index, file_type, escape_str(string), ""]
                        )


def patch_bundle() -> None:
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not BUNDLE_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", BUNDLE_PATH)
        exit(0)

    if not DLC_BUNDLE_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", DLC_BUNDLE_PATH)
        exit(0)

    if not JSON_PATCHED_PATH.exists():
        JSON_PATCHED_PATH.mkdir(parents=True)

    buf = {}

    with CSVReader(BUNDLE_PATH) as csv_reader:
        for row in csv_reader:
            file_index = row[0]
            source_language = row[2]
            destination_language = row[3] or source_language

            if destination_language == "$NONE":
                destination_language = ""

            if file_index not in buf:
                buf[file_index] = []

            buf[file_index].append(scape_str(destination_language))

    with CSVReader(DLC_BUNDLE_PATH) as dlc_csv_reader:
        for dlc_row in dlc_csv_reader:
            dlc_file_index = dlc_row[0]
            dlc_source_language = dlc_row[2]
            dlc_destination_language = dlc_row[3] or dlc_source_language

            if dlc_destination_language == "$NONE":
                dlc_destination_language = ""

            if dlc_file_index not in buf:
                buf[dlc_file_index] = []

            buf[dlc_file_index].append(scape_str(dlc_destination_language))

    for json_path in JSON_RAW_PATH.glob("*.json"):
        patched_path = to_json_patched_path(json_path)
        with JsonReader[AbstractCompressionModel](json_path) as model:
            file_index = json_path.stem
            try:
                model.patch(buf[file_index])
            except KeyError:
                continue
            with JsonWriter[AbstractCompressionModel](patched_path) as writer:
                writer.write(model)
                writer.close()
