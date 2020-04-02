from __future__ import annotations
from ImagingS.core import Point
import numpy as np
from typing import Optional, Dict
from math import cos, sin
from ImagingS.core.transform import MatrixTransform


class SkewTransform(MatrixTransform):
    def __init__(self) -> None:
        super().__init__()
        self.center = Point()
        self._angle_x = 0
        self.angle_y = 0

    @staticmethod
    def create(center: Point, angle_x: float, angle_y: float) -> SkewTransform:
        result = SkewTransform()
        result.center = center
        result.angle_x = angle_x
        result.angle_y = angle_y
        return result
    
    def __update_matrix(self) -> None:
        self.matrix = np.array(
            [[cos(self._angle_y), sin(self._angle_x)],
             [sin(self._angle_y), cos(self._angle_x)]])

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, value: Point) -> None:
        self._center = value

    @property
    def angle_x(self) -> float:
        return self._angle_x

    @angle_x.setter
    def angle_x(self, value: float) -> None:
        self._angle_x = value
        self.__update_matrix()

    @property
    def angle_y(self) -> float:
        return self._angle_y

    @angle_y.setter
    def angle_y(self, value: float) -> None:
        self._angle_y = value
        self.__update_matrix()

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
