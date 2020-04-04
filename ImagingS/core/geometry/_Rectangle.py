from __future__ import annotations
from typing import Dict
from ImagingS.core import Point, RectArea
from . import Polygon


class Rectangle(Polygon):
    def __init__(self) -> None:
        super().__init__()
        self.area = RectArea()

    @staticmethod
    def create(area: RectArea, algorithm: str) -> Rectangle:
        result = Rectangle()
        result.area = area
        result.algorithm = algorithm
        return result

    @property
    def area(self) -> RectArea:
        return self._area

    @area.setter
    def area(self, value: RectArea) -> None:
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
        if Polygon.S_Vertexes in result:
            del result[Polygon.S_Vertexes]
        return result
