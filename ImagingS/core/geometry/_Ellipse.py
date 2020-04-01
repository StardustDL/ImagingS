from typing import Dict, Any
from ImagingS.core import RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class Ellipse(Geometry):
    def __init__(self, area: RectArea) -> None:
        super().__init__()
        self.area = area

    def render(self, context: DrawingContext) -> None:
        raise NotImplementedError()

    def boundingArea(self, context: DrawingContext) -> RectArea:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: Dict) -> Any:
        raise NotImplementedError()
