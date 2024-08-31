from app.utils.path import (
    to_json_patched_path,
    JSON_RAW_PATH,
    BUNDLE_PATH,
    CSV_PATH,
    JSON_PATCHED_PATH,
    VARS_PATH,
    FIXES_PATH,
)
from app.utils.string import escape_str, scape_str
from app.csv.vars import Variables
from app.csv.fixes import Fixes
from app.binary.compression.base import AbstractCompressionModel
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

    unique_strings = []

    print(
        f"{Fore.GREEN}[Save bundle]:{Style.RESET_ALL}",
        BUNDLE_PATH,
    )

    with CSVWriter(BUNDLE_PATH) as writer:
        for file_path in JSON_RAW_PATH.glob("*.json"):
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
    if not JSON_RAW_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", JSON_RAW_PATH)
        exit(0)

    if not BUNDLE_PATH.exists():
        print(f"{Fore.RED}[Not found]:{Style.RESET_ALL}", BUNDLE_PATH)
        exit(0)

    if not JSON_PATCHED_PATH.exists():
        JSON_PATCHED_PATH.mkdir(parents=True)

    vars = None
    fixes = None
    patches = []

    if VARS_PATH.exists():
        vars = Variables()
        vars.load()

    if FIXES_PATH.exists():
        fixes = Fixes()
        fixes.load()

    with CSVReader(BUNDLE_PATH) as reader:
        for row in reader:
            raw, translated = row
            if translated and translated != "":
                if vars:
                    translated = vars.parse(translated)
                patches.append((raw, translated))

    for file_path in JSON_RAW_PATH.glob("*.json"):
        patched_path = to_json_patched_path(file_path)
        file_index = int(file_path.stem)
        with JsonReader[AbstractCompressionModel](file_path) as model:
            with JsonWriter[AbstractCompressionModel](patched_path) as writer:
                print(
                    f"{Fore.GREEN}[Patch model]:{Style.RESET_ALL}",
                    file_path,
                    "->",
                    patched_path,
                    f"{Fore.CYAN}({model.__class__.__name__}){Style.RESET_ALL}",
                )
                for patch in patches:
                    raw, translated = patch
                    model.apply_patch((scape_str(raw), scape_str(translated)))
                if fixes:
                    for fix in fixes.items:
                        if file_index == int(fix[0]):
                            print(f"{Fore.GREEN}[Apply fix]:{Style.RESET_ALL}", fix)
                            model.apply_fix(fix)
                writer.write(model)
