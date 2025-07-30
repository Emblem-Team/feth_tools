from feth.utils.path import (
    PACKAGE_PATH,
    NX_PATH,
    EMU_PATH,
    NX_README_PATH,
    EMU_README_PATH,
    ATMO_PATH,
    LAYRED_FS_PATH,
    DATA_PATH,
)

import shutil
import zipfile
import os

NX_README = [
    "Русификатор для игры Fire Emblem: Three Houses",
    "Версия: {}",
    "Авторы: https://vk.com/emblem_team",
    "Установка: Удалить предыдущую версию русификатора и скопировать папку atmosphere на SD карту вашей консоли",
    "!! Внимание !! У вас должно быть установлено обновление 1.2.0",
    "Игра переведена на 98%. DLC на данный момент не переведены",
]
EMU_README = [
    "Русификатор для игры Fire Emblem: Three Houses",
    "Версия: {}",
    "Авторы: https://vk.com/emblem_team",
    "Установка: Скопировать папку FE3H_Russian_Translation_{} в папку модов на эмуляторе и удалить (или выключить) предыдущую версию русификатора",
    "!! Внимание !! У вас должно быть установлено обновление 1.2.0",
    "Игра переведена на 98%. DLC на данный момент не переведены",
]


def make_nx_arch(version: str):
    emu_mod_path = EMU_PATH / "FE3H_Russian_Translation_{}".format(version)
    if PACKAGE_PATH.exists():
        shutil.rmtree(PACKAGE_PATH)

    NX_PATH.mkdir(parents=True)
    EMU_PATH.mkdir(parents=True)
    ATMO_PATH.mkdir(parents=True)
    emu_mod_path.mkdir(parents=True)

    NX_README[1] = NX_README[1].format(version)
    EMU_README[1] = EMU_README[1].format(version)
    EMU_README[3] = EMU_README[3].format(version)

    NX_README_PATH.write_text("\n\n".join(NX_README))
    EMU_README_PATH.write_text("\n\n".join(EMU_README))

    shutil.copytree(LAYRED_FS_PATH, emu_mod_path / "romfs")
    shutil.copytree(LAYRED_FS_PATH, ATMO_PATH / "romfs")

    emu_arch_path = DATA_PATH / "FE3H_Russian_Translation_{}_emu.zip".format(version)
    nx_arch_path = DATA_PATH / "FE3H_Russian_Translation_{}_nx.zip".format(version)

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
