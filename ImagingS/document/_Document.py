from __future__ import annotations
from ImagingS.core.drawing import Drawing
from typing import List, Dict, Any
from ImagingS.core.brush import Brush
from . import Serializable
from .json import Decoder, Encoder
import json


class Document(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.brushes: List[Brush] = []
        self.drawings: List[Drawing] = []

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = Document()
        result.__dict__ = data

    def save(self, file) -> None:
        json.dump(self, file, ensure_ascii=False, cls=Encoder)

    @staticmethod
    def load(file) -> Document:
        return json.load(file, cls=Decoder)
