from __future__ import annotations

import json
import lzma
import uuid
from enum import IntEnum, unique
from typing import List

from ImagingS import IdObject, Size
from ImagingS.brush import Brush
from ImagingS.drawing import DrawingGroup
from ImagingS.serialization import PropertySerializable
from ImagingS.serialization.json import Decoder, Encoder


@unique
class DocumentFormat(IntEnum):
    ISD = 1
    RAW = 2


class Document(PropertySerializable, IdObject):
    def __init__(self) -> None:
        super().__init__()
        self.id = str(uuid.uuid1())
        self.brushes = []
        self.drawings = DrawingGroup()
        self.size = Size.create(600, 600)

    @property
    def brushes(self) -> List[Brush]:
        return self._brushes

    @brushes.setter
    def brushes(self, value: List[Brush]) -> None:
        self._brushes = value

    @property
    def drawings(self) -> DrawingGroup:
        return self._drawings

    @drawings.setter
    def drawings(self, value: DrawingGroup) -> None:
        self._drawings = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        self._size = value

    def save(self, file, format: DocumentFormat = DocumentFormat.ISD) -> None:
        if type is DocumentFormat.RAW:
            json.dump(self, file, ensure_ascii=False, indent=4, cls=Encoder)
        else:
            s = json.dumps(self, ensure_ascii=False, cls=Encoder)
            data = s.encode("utf8")
            data = lzma.compress(data)
            file.write(data)

    @staticmethod
    def load(file, format: DocumentFormat = DocumentFormat.ISD) -> Document:
        if type is DocumentFormat.RAW:
            return json.load(file, cls=Decoder)
        else:
            data = file.read()
            data = lzma.decompress(data)
            s = data.decode("utf8")
            return json.loads(s, cls=Decoder)
