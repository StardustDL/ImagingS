from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ImagingS import Point

from . import MatrixTransform


class TranslateTransform(MatrixTransform):
    def __init__(self, delta: Optional[Point] = None) -> None:
        super().__init__()
        self.delta = delta if delta else Point()

    @property
    def delta(self) -> Point:
        return self._delta

    @delta.setter
    def delta(self, value: Point) -> None:
        assert isinstance(value, Point)
        self._delta = value
        self.matrix = np.array(
            [[1, 0, 0],
             [0, 1, 0],
             [self._delta.x, self._delta.y, 1]])

    def transform(self, origin: Point) -> Point:
        return origin + self._delta

    def serialize(self) -> Dict:
        result = super().serialize()
        if MatrixTransform.S_Matrix in result:
            del result[MatrixTransform.S_Matrix]
        return result
