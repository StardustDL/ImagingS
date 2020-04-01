from ImagingS.core import Point
import numpy as np
from typing import Optional
from math import cos, sin
from ImagingS.core.transform import MatrixTransform


class RotateTransform(MatrixTransform):
    def __init__(self, center: Point, angle: float) -> None:
        super().__init__(np.array(
            [[cos(angle), -sin(angle)],
             [sin(angle), cos(angle)]]))
        self._center = center
        self._angle = angle

    @property
    def center(self) -> Point:
        return self._center

    @property
    def angle(self) -> float:
        return self._angle

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)
