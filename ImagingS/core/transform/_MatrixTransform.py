import numpy as np
from typing import Optional, Dict, Any
from ImagingS.core import Point
from . import Transform


class MatrixTransform(Transform):
    def __init__(self, matrix: np.ndarray) -> None:
        super().__init__()
        self._matrix = matrix

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix

    @matrix.setter
    def matrix(self, value: np.ndarray) -> None:
        self._matrix = value

    def transform(self, origin: Point) -> Optional[Point]:
        return Point.from_array(np.dot(self._matrix, origin.to_array()))

    def serialize(self) -> Dict:
        return {
            "00": self.matrix[0][0],
            "01": self.matrix[0][1],
            "10": self.matrix[1][0],
            "11": self.matrix[1][1],
        }

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = MatrixTransform(np.array([
            [data["00"], data["01"]],
            [data["10"], data["11"]]
        ]))
        return result
