from pathlib import Path
from iostuff.readers.csv import CSVReader
from iostuff.writers.csv import CSVWriter


def merge_bundles(src_bundle_path: Path, dest_bundle_path: Path, out_bundle_path: Path):
    source = []
    dest = []
    with CSVReader(src_bundle_path) as src_reader:
        for row in src_reader:
            source.append(row)
    with CSVReader(dest_bundle_path) as dest_reader:
        for row in dest_reader:
            dest.append(row)
    for src_idx, src_row in enumerate(source):
        for dest_idx, dest_row in enumerate(dest):
            if src_row[2] == dest_row[2]:
                source[src_idx][3] = dest[dest_idx][3]

    with CSVWriter(out_bundle_path) as out_writer:
        for row in source:
            out_writer.write_row(row)
