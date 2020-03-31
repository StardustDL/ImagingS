import numpy as np
from typing import Optional
from ImagingS.core import Point
from . import Transform


class Matrix(Transform):
    def __init__(self, matrix: np.matrix) -> None:
        super().__init__()
        self._matrix = matrix

    @property
    def matrix(self) -> np.matrix:
        return self._matrix

    def transform(self, origin: Point) -> Optional[Point]:
        return self._matrix * origin.to_array()
