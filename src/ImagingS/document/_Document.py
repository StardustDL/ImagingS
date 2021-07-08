from __future__ import annotations

import json
import lzma
import uuid
from enum import Enum, unique

from ImagingS import IdObject, IdObjectList, Size
from ImagingS.brush import Brush
from ImagingS.drawing import DrawingGroup
from ImagingS.serialization import PropertySerializable
from ImagingS.serialization.json import Decoder, Encoder


@unique
class DocumentFormat(Enum):
    ISD = 1
    RAW = 2


class Document(PropertySerializable, IdObject):
    def __init__(self) -> None:
        super().__init__()
        self.id = str(uuid.uuid1())
        self.brushes = IdObjectList()
        self.drawings = DrawingGroup()
        self.size = Size(600, 600)

    @property
    def brushes(self) -> IdObjectList[Brush]:
        return self._brushes

    @brushes.setter
    def brushes(self, value: IdObjectList[Brush]) -> None:
        assert isinstance(value, IdObjectList)
        self._brushes = value

    @property
    def drawings(self) -> DrawingGroup:
        return self._drawings

    @drawings.setter
    def drawings(self, value: DrawingGroup) -> None:
        assert isinstance(value, DrawingGroup)
        self._drawings = value

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value: Size) -> None:
        assert isinstance(value, Size)
        self._size = value

    def save(self, file, format: DocumentFormat = DocumentFormat.ISD) -> None:
        if format is DocumentFormat.RAW:
            json.dump(self, file, ensure_ascii=False, indent=4, cls=Encoder)
        else:
            s = json.dumps(self, ensure_ascii=False, cls=Encoder)
            data = s.encode("utf8")
            data = lzma.compress(data)
            file.write(data)

    @staticmethod
    def load(file, format: DocumentFormat = DocumentFormat.ISD) -> Document:
        if format is DocumentFormat.RAW:
            result = json.load(file, cls=Decoder)
        else:
            data = file.read()
            data = lzma.decompress(data)
            s = data.decode("utf8")
            result = json.loads(s, cls=Decoder)
        assert isinstance(result, Document)
        return result
