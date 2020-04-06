from __future__ import annotations

from ImagingS.core import Point

from . import Transform


class TranslateTransform(Transform):
    def __init__(self) -> None:
        super().__init__()
        self.delta = Point()

    @staticmethod
    def create(delta: Point) -> TranslateTransform:
        result = TranslateTransform()
        result.delta = delta
        return result

    @property
    def delta(self) -> Point:
        return self._delta

    @delta.setter
    def delta(self, value: Point) -> None:
        self._delta = value

    def transform(self, origin: Point) -> Point:
        return origin + self._delta
