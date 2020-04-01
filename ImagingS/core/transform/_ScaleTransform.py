from ImagingS.core import Point
from typing import Optional, Dict, Any
import numpy as np
from ImagingS.core.transform import MatrixTransform


class ScaleTransform(MatrixTransform):
    def __init__(self, center: Point, factor: float) -> None:
        super().__init__(np.array(
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

    def transform(self, origin: Point) -> Optional[Point]:
        return super().transform(origin - self._center)

    def serialize(self) -> Dict:
        return {
            "_center": self._center,
            "_factor": self._factor
        }

    @staticmethod
    def deserialize(data: Dict) -> Any:
        result = ScaleTransform(data["_center"], data["_factor"])
        return result
