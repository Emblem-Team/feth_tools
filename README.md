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

#### Create and activate env

```
python -m venv .venv
source .venv/bin/activate (unix,mac) or .venv\Scripts\activate (windows)
```

#### Install deps

```
pip install -r requirements.txt
```

#### Create .env file and fill your data

```
copy .env.example .env
```

#### Init tools

```
python -m feth init
```

#### Build

```
python -m feth build
```

#### Show all commands

```
python -m feth
```
