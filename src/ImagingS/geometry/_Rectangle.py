from __future__ import annotations

from typing import Dict, Optional, cast

from ImagingS import Point, Rect

from . import LineAlgorithm, PolygonGeometry


class RectangleGeometry(PolygonGeometry):
    def __init__(self, rect: Optional[Rect] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__(algorithm=algorithm)
        self.rect = rect if rect else Rect()

    @property
    def rect(self) -> Rect:
        return self._rect

    @rect.setter
    def rect(self, value: Rect) -> None:
        assert isinstance(value, Rect)
        self._rect = value
        self.vertexes = [
            self._rect.origin,
            self._rect.origin + Point(self._rect.size.width, 0),
            self._rect.origin +
            Point(self._rect.size.width, self._rect.size.height),
            self._rect.origin + Point(0, self._rect.size.height),
        ]

    def serialize(self) -> Dict:
        result = super().serialize()
        if PolygonGeometry.S_Vertexes in result:
            del result[PolygonGeometry.S_Vertexes]
        return result

    def _calculateBounds(self) -> Rect:
        if self.transform is not None:
            target = cast(PolygonGeometry, self.transformed())
            return target._calculateBounds()
        else:
            return self.rect
