from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from iostuff.readers.binary import BinaryReader
    from iostuff.writers.binary import BinaryWriter


class AbstractCompressionModel(ABC):
    @abstractmethod
    def get_strings(self) -> list[str]:
        pass

    @abstractmethod
    def apply_patch(self, patch: tuple[str, str]) -> None:
        pass

    @abstractmethod
    def apply_fix(self, fix: list) -> None:
        pass


class AbstractCompressionType(ABC):
    indexes: list[int]

    @abstractmethod
    def unpack(self, reader: BinaryReader) -> AbstractCompressionModel:
        pass

    def pack(self, model: AbstractCompressionModel, writer: BinaryWriter) -> None:
        pass
