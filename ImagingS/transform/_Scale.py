from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from ImagingS import Point
from ImagingS.transform import MatrixTransform


class ScaleTransform(MatrixTransform):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self.factor = (1, 1)

    @staticmethod
    def create(center: Point, factor: Tuple[float, float]) -> ScaleTransform:
        result = ScaleTransform()
        result.center = center
        result.factor = factor
        return result

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        self._center = value

    @property
    def factor(self) -> Tuple[float, float]:
        return self._factor

    @factor.setter
    def factor(self, value: Tuple[float, float]) -> None:
        self._factor = value
        self.matrix = np.array(
            [[self._factor[0], 0, 0],
             [0, self._factor[1], 0],
             [0, 0, 1]])

    def transform(self, origin: Point) -> Point:
        return super().transform(origin - self._center) + self.center

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
