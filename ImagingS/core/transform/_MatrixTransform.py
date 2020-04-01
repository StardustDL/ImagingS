from __future__ import annotations
import numpy as np
from typing import Optional, Dict
from ImagingS.core import Point
from . import Transform


class MatrixTransform(Transform):
    S_Matrix = "_matrix"

    def __init__(self) -> None:
        super().__init__()
        self.matrix = np.eye(2)

    @staticmethod
    def create(matrix: np.ndarray) -> MatrixTransform:
        result = MatrixTransform()
        result.matrix = matrix
        return result

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix

    @matrix.setter
    def matrix(self, value: np.ndarray) -> None:
        self._matrix = value

    def transform(self, origin: Point) -> Optional[Point]:
        return Point.from_array(np.dot(self._matrix, origin.to_array()))

    def serialize(self) -> Dict:
        result = super().serialize()

        if "matrix" in result:
            del result["matrix"]

        result[self.S_Matrix] = [self.matrix[0][0], self.matrix[0][1],
                                 self.matrix[1][0], self.matrix[1][1]]
        return result

    def deserialize(self, data: Dict) -> None:
        if self.S_Matrix in data:
            mat = data[self.S_Matrix]
            self.matrix = np.array([[mat[0], mat[1]], [mat[2], mat[3]]])
