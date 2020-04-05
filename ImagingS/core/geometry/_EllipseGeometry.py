from __future__ import annotations
from ImagingS.core import RectArea
from ImagingS.core.drawing import DrawingContext
from . import Geometry


class EllipseGeometry(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.area = RectArea()

    @staticmethod
    def create(area: RectArea) -> EllipseGeometry:
        result = EllipseGeometry()
        result.area = area
        return result

    @property
    def area(self) -> RectArea:
        return self._area

    @area.setter
    def area(self, value: RectArea) -> None:
        self._area = value

    def render(self, context: DrawingContext) -> None:
        pass
