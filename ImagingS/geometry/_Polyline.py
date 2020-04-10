from __future__ import annotations

from typing import Iterable, List, Optional

from ImagingS import Point
from ImagingS.drawing import Pen

from . import Geometry, LineAlgorithm, LineGeometry


class PolylineGeometry(Geometry):
    S_Vertexes = "vertexes"

    def __init__(self, vertexes: Optional[List[Point]] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__()
        self.vertexes = vertexes if vertexes else []
        self.algorithm = algorithm if algorithm else LineAlgorithm.Dda

    @property
    def algorithm(self) -> LineAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: LineAlgorithm) -> None:
        assert isinstance(value, LineAlgorithm)
        self._algorithm = value

    @property
    def vertexes(self) -> List[Point]:
        return self._vertexes

    @vertexes.setter
    def vertexes(self, value: List[Point]) -> None:
        assert isinstance(value, list)
        self._vertexes = value

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        cnt = len(self.vertexes)
        if cnt == 0:
            return
        for i in range(cnt - 1):
            ln = LineGeometry(self.vertexes[i],
                              self.vertexes[i+1], self.algorithm)
            ln.transform = self.transform
            for point in ln.strokePoints(pen):
                yield point

    def fillPoints(self) -> Iterable[Point]:
        return []


class PolygonGeometry(PolylineGeometry):
    def __init__(self, vertexes: Optional[List[Point]] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__(vertexes, algorithm)

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        cnt = len(self.vertexes)
        if cnt > 0:
            for point in super().strokePoints(pen):
                yield point
            ln = LineGeometry(self.vertexes[-1],
                              self.vertexes[0], self.algorithm)
            ln.transform = self.transform
            for point in ln.strokePoints(pen):
                yield point
