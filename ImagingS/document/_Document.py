from __future__ import annotations
from ImagingS.core import IdObjectList
from ImagingS.core.drawing import Drawing
from typing import Dict, Any
from ImagingS.core.brush import Brush
from ImagingS.core.serialization import Serializable
from ImagingS.core.serialization.json import Decoder, Encoder
import json


class Document(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.brushes: IdObjectList[Brush] = IdObjectList()
        self.drawings: IdObjectList[Drawing] = IdObjectList()

    def serialize(self) -> Dict:
        return {
            "brushes": self.brushes.items,
            "drawings": self.drawings.items
        }

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = Document()
        result.brushes = IdObjectList(data["brushes"])
        result.drawings = IdObjectList(data["drawings"])
        return result

    def save(self, file) -> None:
        json.dump(self, file, ensure_ascii=False, indent=4, cls=Encoder)

    @staticmethod
    def load(file) -> Document:
        return json.load(file, cls=Decoder)
