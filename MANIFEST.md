# Manifest Format Specification

This document describes the `manifest.json` file used by the **translation tooling** when building distribution packages for the translation mod of _Fire Emblem: Three Houses_. During the build process, this file is read, processed (version placeholders are replaced), and then embedded into the final archives (e.g., for Nintendo Switch or emulators).

## Purpose

- Defines the current version of the translation mod.
- Holds platform‑specific readme content that will be written into the final `README.txt` file for each target platform.
- Inside any string of the nx or emu arrays, you may use the placeholder **{}**.
- At build time, every occurrence of **{}** will be replaced with the value of the version field.

## Structure

The root object has **two required fields**:

```json
{
  "version": "string",
  "readme": {
    "nx": ["string", ...],
    "emu": ["string", ...]
  }
}
```

## Example

```json
{
  "version": "1.0.2",
  "readme": {
    "nx": [
      "Русификатор для игры Fire Emblem: Three Houses",
      "Версия: {}",
      "Авторы: https://vk.com/emblem_team",
      "Установка: Удалить предыдущую версию русификатора и скопировать папку atmosphere на SD карту вашей консоли",
      "!! Внимание !! У вас должно быть установлено обновление 1.2.0",
      "Игра переведена на 100%. DLC переведён на 28%"
    ],
    "emu": [
      "Русификатор для игры Fire Emblem: Three Houses",
      "Версия: {}",
      "Авторы: https://vk.com/emblem_team",
      "Установка: Скопировать папку FE3H_Russian_Translation_{} в папку модов на эмуляторе и удалить (или выключить) предыдущую версию русификатора",
      "!! Внимание !! У вас должно быть установлено обновление 1.2.0",
      "Игра переведена на 100%. DLC переведён на 28%"
    ]
  }
}
```
