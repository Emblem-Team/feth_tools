from feth.utils.path import (
    WORKDIR_PATH,
    PACKAGE_PATH,
    NX_PATH,
    EMU_PATH,
    NX_README_PATH,
    EMU_README_PATH,
    ATMO_PATH,
    LAYERED_FS_PATH,
)

from .manifest import parse_manifest, Manifest

import shutil
import zipfile
import os


def make_distr(manifest: Manifest):
    manifest = parse_manifest()
    emu_mod_path = EMU_PATH / "{}_{}".format(manifest.prefix, manifest.version)
    if PACKAGE_PATH.exists():
        shutil.rmtree(PACKAGE_PATH)

    NX_PATH.mkdir(parents=True)
    EMU_PATH.mkdir(parents=True)
    ATMO_PATH.mkdir(parents=True)
    emu_mod_path.mkdir(parents=True)

    for idx, _ in enumerate(manifest.nx_readme):
        manifest.nx_readme[idx] = manifest.nx_readme[idx].format(manifest.version)

    for idx, _ in enumerate(manifest.emu_readme):
        manifest.emu_readme[idx] = manifest.emu_readme[idx].format(manifest.version)

    NX_README_PATH.write_text("\n\n".join(manifest.nx_readme))
    EMU_README_PATH.write_text("\n\n".join(manifest.emu_readme))

    shutil.copytree(LAYERED_FS_PATH, emu_mod_path / "romfs")
    shutil.copytree(LAYERED_FS_PATH, ATMO_PATH / "romfs")


def make_nx_arch(manifest: Manifest):
    emu_arch_path = WORKDIR_PATH / "{}_{}_emu.zip".format(
        manifest.prefix, manifest.version
    )
    nx_arch_path = WORKDIR_PATH / "{}_{}_nx.zip".format(
        manifest.prefix, manifest.version
    )

    with zipfile.ZipFile(emu_arch_path, "w", zipfile.ZIP_DEFLATED) as fd:
        for root, dirs, files in os.walk(EMU_PATH):
            for file in files:
                path = os.path.join(root, file)
                arcname = os.path.relpath(path, EMU_PATH)
                fd.write(path, arcname=arcname)
    with zipfile.ZipFile(nx_arch_path, "w", zipfile.ZIP_DEFLATED) as fd:
        for root, dirs, files in os.walk(NX_PATH):
            for file in files:
                path = os.path.join(root, file)
                arcname = os.path.relpath(path, NX_PATH)
                fd.write(path, arcname=arcname)
