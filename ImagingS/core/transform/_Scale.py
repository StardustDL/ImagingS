from __future__ import annotations
from ImagingS.core import Point
from typing import Optional, Dict
import numpy as np
from ImagingS.core.transform import MatrixTransform


class ScaleTransform(MatrixTransform):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self.factor = 1

    @staticmethod
    def create(center: Point, factor: float) -> ScaleTransform:
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
    def factor(self) -> float:
        return self._factor

    @factor.setter
    def factor(self, value: float) -> None:
        self._factor = value
        self.matrix = np.array(
            [[self._factor, 0],
             [0, self._factor]])

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
