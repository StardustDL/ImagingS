from __future__ import annotations
from ImagingS.core import Point
import numpy as np
from typing import Optional, Dict
from math import cos, sin
from ImagingS.core.transform import MatrixTransform


class RotateTransform(MatrixTransform):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self.angle = 0

    @staticmethod
    def create(center: Point, angle: float) -> RotateTransform:
        result = RotateTransform()
        result.center = center
        result.angle = angle
        return result

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        self._center = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value
        self.matrix = np.array(
            [[cos(self._angle), -sin(self._angle)],
             [sin(self._angle), cos(self._angle)]])

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
