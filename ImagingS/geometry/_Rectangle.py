from __future__ import annotations

from typing import Dict

from ImagingS import Point, Rect

from . import LineAlgorithm, PolygonGeometry


class RectangleGeometry(PolygonGeometry):
    def __init__(self) -> None:
        super().__init__()
        self.rect = Rect()

    @staticmethod
    def create(rect: Rect, algorithm: LineAlgorithm) -> RectangleGeometry:
        result = RectangleGeometry()
        result.rect = rect
        result.algorithm = algorithm
        return result

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect) -> None:
        self._rect = value
        self.vertexes = [
            self._rect.origin,
            self._rect.origin + Point.create(self._rect.size.width, 0),
            self._rect.origin +
            Point.create(self._rect.size.width, self._rect.size.height),
            self._rect.origin + Point.create(0, self._rect.size.height),
        ]

    def serialize(self) -> Dict:
        result = super().serialize()
        if PolygonGeometry.S_Vertexes in result:
            del result[PolygonGeometry.S_Vertexes]
        return result
