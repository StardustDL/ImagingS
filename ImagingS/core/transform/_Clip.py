from __future__ import annotations
from ImagingS.core import RectArea, Point
from . import Transform


class ClipTransform(Transform):
    def __init__(self) -> None:
        super().__init__()
        self.area = RectArea()
        self.algorithm = "Cohen-Sutherland"

    @staticmethod
    def create(area: RectArea, algorithm: str) -> ClipTransform:
        result = ClipTransform()
        result.area = area
        result.algorithm = algorithm
        return result

    @property
    def area(self) -> RectArea:
        return self._area

    @area.setter
    def area(self, value: RectArea) -> None:
        self._area = value

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: str) -> None:
        self._algorithm = value

    def transform(self, origin: Point) -> Point:
        return origin
