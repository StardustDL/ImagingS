from __future__ import annotations

from math import cos, sin
from typing import Dict, Optional

import numpy as np

from ImagingS import Point
from ImagingS.transform import MatrixTransform


class RotateTransform(MatrixTransform):
    def __init__(self, center: Optional[Point] = None, angle: float = 0.0) -> None:
        super().__init__()
        self.center = center if center else Point()
        self.angle = angle

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._center = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = float(value)
        self.matrix = np.array(
            [[cos(self._angle), -sin(self._angle), 0],
             [sin(self._angle), cos(self._angle), 0],
             [0, 0, 1]])

    def transform(self, origin: Point) -> Point:
        return super().transform(origin - self.center) + self.center

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
