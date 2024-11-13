from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter

from zlib import decompress, compress
from pathlib import Path


class Block:
    size: int
    data: bytes


class GZFile:
    block_size: int
    block_count: int
    total_size: int
    block_sizes: list[int]
    blocks: list[Block]
    data: bytes


HEADER_SIZE = 0x4
COMPRESSION_LEVEL = 0x9
ENTRY_BLOCK_SIZE = 0x80
BLOCK_SIZE = 0x10000


def read_zlib_block(reader: BinaryReader) -> Block:
    reader.align(ENTRY_BLOCK_SIZE)
    block = Block()
    block.size = reader.read_uint()
    block.data = decompress(reader.read(block.size))
    return block


def read_block(reader: BinaryReader) -> Block:
    reader.align(ENTRY_BLOCK_SIZE)
    block = Block()
    block.size = reader.read_uint()
    block.data = reader.read(block.size)
    return block


def write_zlib_block(reader: BinaryReader, size: int) -> Block:
    block = Block()
    block.data = compress(reader.read(size), COMPRESSION_LEVEL)
    block.size = len(block.data) + HEADER_SIZE
    return block


def decompress_gz(input_file: Path, output_file: Path) -> None:
    print("[Decompress gz]:", input_file, "->", output_file)
    with BinaryReader(input_file) as reader:
        file = GZFile()
        file.block_size = reader.read_uint()
        file.block_count = reader.read_uint()
        file.total_size = reader.read_uint()
        file.data = bytes()

        file.block_sizes = []
        for _ in range(file.block_count):
            file.block_sizes.append(reader.read_uint())

        for _ in range(file.block_count - 1):
            block = read_zlib_block(reader)
            file.data += block.data

        # https://github.com/3096/koeipy/blob/master/koeipy/kt_gz.py#L69
        last_block_size = file.block_sizes[-1:][0]
        if last_block_size == file.total_size - file.block_size * (
            file.block_count - 1
        ):
            block = read_block(reader)
            file.data += block.data
        else:
            block = read_zlib_block(reader)
            file.data += block.data

        with BinaryWriter(output_file) as writer:
            writer.write(file.data)


def compress_gz(input_file: Path, output_file: Path) -> None:
    print("[Compress gz]:", input_file, "->", output_file)
    with BinaryReader(input_file) as reader:
        with BinaryWriter(output_file) as writer:
            file = GZFile()
            file.block_size = BLOCK_SIZE
            file.total_size = input_file.stat().st_size
            file.block_count = (file.total_size - 1) // file.block_size + 1

            file.blocks = []
            for _ in range(file.block_count):
                block = write_zlib_block(reader, file.block_size)
                file.blocks.append(block)

            writer.write_uint(file.block_size)
            writer.write_uint(file.block_count)
            writer.write_uint(file.total_size)

            for block in file.blocks:
                writer.write_uint(block.size)

            for block in file.blocks:
                writer.align(ENTRY_BLOCK_SIZE)
                writer.write_uint(block.size - HEADER_SIZE)
                writer.write(block.data)
