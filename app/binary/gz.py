from iostuff.readers.binary import BinaryReader
from iostuff.writers.binary import BinaryWriter

from zlib import decompress, compress
from os.path import getsize


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


def read_zlib_block(reader: BinaryReader) -> Block:
    reader.align(0x80)
    block = Block()
    block.size = reader.read_uint()
    block.data = decompress(reader.read(block.size))
    return block


def read_block(reader: BinaryReader) -> Block:
    reader.align(0x80)
    block = Block()
    block.size = reader.read_uint()
    block.data = reader.read(block.size)
    return block


def write_zlib_block(reader: BinaryReader, size: int) -> Block:
    block = Block()
    block.data = compress(reader.read(size), 9)
    block.size = len(block.data) + 4
    return block


def decompress_gz(input_file: str, output_file: str) -> None:
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
        if last_block_size == file.total_size - file.block_size * (file.block_count - 1):
            block = read_block(reader)
            file.data += block.data
        else:
            block = read_zlib_block(reader)
            file.data += block.data

        with BinaryWriter(output_file) as writer:
            writer.write(file.data)


def compress_gz(input_file: str, output_file: str) -> None:
    print("[Compress gz]:", input_file, "->", output_file)
    with BinaryReader(input_file) as reader:
        with BinaryWriter(output_file) as writer:
            file = GZFile()
            file.block_size = 0x10000
            file.total_size = getsize(input_file)
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
                writer.align(0x80)
                writer.write_uint(block.size - 4)
                writer.write(block.data)
