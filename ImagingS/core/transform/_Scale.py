from ImagingS.core import Point
import numpy as np
from . import Matrix


class Scale(Matrix):
    def __init__(self, center: Point, factor: float) -> None:
        super().__init__(np.matrix(
            [[factor, 0],
             [0, factor]]))
        self._center = center
        self._factor = factor

    @property
    def center(self) -> Point:
        return self._center

    @property
    def factor(self) -> float:
        return self._factor
