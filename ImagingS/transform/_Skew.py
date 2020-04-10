from __future__ import annotations

from math import tan
from typing import Dict, Tuple

import numpy as np

from ImagingS import Point
from ImagingS.transform import MatrixTransform


class SkewTransform(MatrixTransform):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self.angle = (0, 0)

    @staticmethod
    def create(center: Point, angle: Tuple[float, float]) -> SkewTransform:
        result = SkewTransform()
        result.center = center
        result.angle = angle
        return result

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._center = value

    @property
    def angle(self) -> Tuple[float, float]:
        return self._angle

    @angle.setter
    def angle(self, value: Tuple[float, float]) -> None:
        assert isinstance(value, tuple) or isinstance(value, list)
        assert len(value) == 2
        self._angle = float(value[0]), float(value[1])
        self.matrix = np.array(
            [[1, tan(self._angle[0]), 0],
             [tan(self._angle[1]), 1, 0],
             [0, 0, 1]])

    def transform(self, origin: Point) -> Point:
        return super().transform(origin - self.center) + self.center

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
