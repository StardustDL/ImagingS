from typing import Optional
from ImagingS.core import Point
from . import Transform


class Translate(Transform):
    def __init__(self, delta: Point) -> None:
        super().__init__()
        self._delta = delta
        self._delta_arr = self._delta.to_array()

    @property
    def delta(self) -> Point:
        return self._delta

    def transform(self, origin: Point) -> Optional[Point]:
        return Point.from_array(origin.to_array() + self._delta_arr)
