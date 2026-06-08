from dataclasses import dataclass
from feth.utils.path import MANIFEST_PATH

import json


@dataclass
class Manifest:
    version: str
    nx_readme: list[str]
    emu_readme: list[str]


def parse_manifest() -> Manifest:
    manifest_contents = MANIFEST_PATH.read_text(encoding="utf-8")
    manifest_json = json.loads(manifest_contents)
    manifest = Manifest(
        version=manifest_json["version"],
        nx_readme=manifest_json["readme"]["nx"],
        emu_readme=manifest_json["readme"]["emu"],
    )
    return manifest
