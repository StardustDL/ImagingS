from __future__ import annotations

from typing import Dict

import numpy as np

from ImagingS import Point

from . import Transform


class MatrixTransform(Transform):
    S_Matrix = "_matrix"

    def __init__(self) -> None:
        super().__init__()
        self.matrix = np.eye(3)

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
        assert value.shape == (3, 3)
        self._matrix = value

    def transform(self, origin: Point) -> Point:
        result = Point.from_homogeneous(
            np.dot(self.matrix, origin.to_homogeneous()))
        return result

    def serialize(self) -> Dict:
        result = super().serialize()

        if "matrix" in result:
            del result["matrix"]

        result[self.S_Matrix] = [*self.matrix[0],
                                 *self.matrix[1], *self.matrix[2]]
        return result

    def deserialize(self, data: Dict) -> None:
        if self.S_Matrix in data:
            mat = data.pop(self.S_Matrix)
            self.matrix = np.array([mat[0:3], mat[3:6], mat[6:9]])
        super().deserialize(data)