from __future__ import annotations
from ImagingS.core import IdObjectList, IdObject, Size
from ImagingS.core.drawing import Drawing
from typing import List
from ImagingS.core.brush import Brush
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.serialization.json import Decoder, Encoder
import json
import uuid


class Document(PropertySerializable, IdObject):
    def __init__(self) -> None:
        super().__init__()
        self.id = str(uuid.uuid1())
        self.brushes = []
        self.drawings = IdObjectList()
        self.size = Size.create(600, 600)

    @property
    def brushes(self) -> List[Brush]:
        return self._brushes

    @brushes.setter
    def brushes(self, value: List[Brush]) -> None:
        self._brushes = value

    @property
    def drawings(self) -> IdObjectList[Drawing]:
        return self._drawings

    @drawings.setter
    def drawings(self, value: IdObjectList[Drawing]) -> None:
        self._drawings = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        self._size = value

    def save(self, file) -> None:
        json.dump(self, file, ensure_ascii=False, indent=4, cls=Encoder)

    @staticmethod
    def load(file) -> Document:
        return json.load(file, cls=Decoder)
