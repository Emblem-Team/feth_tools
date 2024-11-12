## Fire Emblem: Three Houses - Translating tools

### Features

- Unpacking all binary files from DATA0/1.bin file
- Updating these files from patch(1-4) files
- Unpacking ENG_E game text and converting to json models
- Creating csv bundle from json models
- Patching json models from csv bundle
- Packing json models into binary
- Decompressing/compressing koei gz
- Unpacking game tutorials (graphic)

### Requirements

- Python 3.12
- DATA0.bin / DATA1.bin
- Patches, if need

### Usage

#### Install deps

```
py -m venv venv
venv\scripts\pip install -r requirements.txt
```

#### Create .env file and fill your data

```
copy .env.example .env
```

#### Init tools

```
venv\scripts\python -m app init
```

#### Build

```
venv\scripts\python -m app build
```

#### Show all commands

```
venv\scripts\python -m app
```
