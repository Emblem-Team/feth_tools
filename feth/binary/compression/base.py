from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from iostuff.readers.binary import BinaryReader
    from iostuff.writers.binary import BinaryWriter


class AbstractCompressionModel(ABC):
    @property
    @abstractmethod
    def strings(self) -> list[str]:
        pass

    @abstractmethod
    def patch(self, strings: list[str]) -> None:
        pass

    @abstractmethod
    def str(self) -> str:
        pass


class AbstractCompressionType(ABC):
    indexes: list[int]

    @abstractmethod
    def unpack(self, reader: BinaryReader) -> AbstractCompressionModel:
        pass

    @abstractmethod
    def pack(self, model: AbstractCompressionModel, writer: BinaryWriter) -> None:
        pass
