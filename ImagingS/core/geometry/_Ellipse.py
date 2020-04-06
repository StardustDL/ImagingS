from __future__ import annotations

from typing import Iterable

from ImagingS.core import Point, Rect
from ImagingS.core.drawing import Pen

from . import Geometry


class EllipseGeometry(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.area = Rect()

    @staticmethod
    def create(area: Rect) -> EllipseGeometry:
        result = EllipseGeometry()
        result.area = area
        return result

    @property
    def area(self) -> Rect:
        return self._area

    @area.setter
    def area(self, value: Rect) -> None:
        self._area = value

    def stroke_points(self, pen: Pen) -> Iterable[Point]:
        return []

    def fill_points(self) -> Iterable[Point]:
        return []
