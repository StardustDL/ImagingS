from __future__ import annotations

import json
import lzma
import uuid
from typing import List

from ImagingS.core import IdObject, Size
from ImagingS.core.brush import Brush
from ImagingS.core.drawing import DrawingGroup
from ImagingS.core.serialization import PropertySerializable
from ImagingS.core.serialization.json import Decoder, Encoder


class Document(PropertySerializable, IdObject):
    FILE_ISD, FILE_RAW = range(2)

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

    def save(self, file, type=0) -> None:
        if type == self.FILE_RAW:
            json.dump(self, file, ensure_ascii=False, indent=4, cls=Encoder)
        else:
            s = json.dumps(self, ensure_ascii=False, cls=Encoder)
            data = s.encode("utf8")
            data = lzma.compress(data)
            file.write(data)

    @classmethod
    def load(cls, file, type=0) -> Document:
        if type == cls.FILE_RAW:
            return json.load(file, cls=Decoder)
        else:
            data = file.read()
            data = lzma.decompress(data)
            s = data.decode("utf8")
            return json.loads(s, cls=Decoder)
