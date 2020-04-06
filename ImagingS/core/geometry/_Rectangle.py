from __future__ import annotations

from typing import Dict

from ImagingS.core import Point, Rect

from . import PolygonGeometry


class RectangleGeometry(PolygonGeometry):
    def __init__(self) -> None:
        super().__init__()
        self.area = Rect()

    @staticmethod
    def create(area: Rect, algorithm: str) -> RectangleGeometry:
        result = RectangleGeometry()
        result.area = area
        result.algorithm = algorithm
        return result

    @property
    def area(self) -> Rect:
        return self._area

    @area.setter
    def area(self, value: Rect) -> None:
        self._area = value
        self.vertexes = [
            self._area.origin,
            self._area.origin + Point.create(self._area.size.width, 0),
            self._area.origin +
            Point.create(self._area.size.width, self._area.size.height),
            self._area.origin + Point.create(0, self._area.size.height),
        ]

    def serialize(self) -> Dict:
        result = super().serialize()
        if PolygonGeometry.S_Vertexes in result:
            del result[PolygonGeometry.S_Vertexes]
        return result
