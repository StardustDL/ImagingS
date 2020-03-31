
from ImagingS.core import Point
import numpy as np
from math import cos, sin
from . import Matrix


class Rotate(Matrix):
    def __init__(self, center: Point, angle: float) -> None:
        # angle: anticlockwise
        super().__init__(np.matrix(
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
