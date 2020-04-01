from ImagingS.core import Point
import numpy as np
from typing import Optional
from math import cos, sin
from ImagingS.core.transform import MatrixTransform


class SkewTransform(MatrixTransform):
    def __init__(self, center: Point, angle_x: float, angle_y: float) -> None:
        super().__init__(np.array(
            [[cos(angle_y), sin(angle_x)],
             [sin(angle_y), cos(angle_x)]]))
        self._center = center
        self._angle_x = angle_x
        self._angle_y = angle_y

    @property
    def center(self) -> Point:
        return self._center

    @property
    def angle_x(self) -> float:
        return self._angle_x

    @property
    def angle_y(self) -> float:
        return self._angle_y

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)
