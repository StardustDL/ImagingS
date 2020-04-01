from typing import Optional
from ImagingS.core import Point
from . import Transform


class TranslateTransform(Transform):
    def __init__(self, delta: Point) -> None:
        super().__init__()
        self._delta = delta

    @property
    def delta(self) -> Point:
        return self._delta

    def transform(self, origin: Point) -> Optional[Point]:
        return origin + self._delta
