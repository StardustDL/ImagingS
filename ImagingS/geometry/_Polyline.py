from __future__ import annotations

from typing import Iterable, List, Optional, cast

from ImagingS import Point, Rect, RectMeasurer
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
        self.refreshBounds()

    def transformed(self) -> Geometry:
        if self.transform is None:
            return self
        else:
            vertexes = list(map(self.transform.transform, self.vertexes))
            return PolylineGeometry(vertexes, self.algorithm)

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        target = self
        if self.transform is not None:
            target = cast(PolylineGeometry, self.transformed())
        cnt = len(target.vertexes)
        if cnt == 0:
            return
        for i in range(cnt - 1):
            ln = LineGeometry(target.vertexes[i],
                              target.vertexes[i+1], target.algorithm)
            for point in ln.strokePoints(pen):
                yield point

    def fillPoints(self) -> Iterable[Point]:
        return []

    def _calculateBounds(self) -> Rect:
        target = self
        if self.transform is not None:
            target = cast(PolylineGeometry, self.transformed())
        measure = RectMeasurer()
        measure.append(target.vertexes)
        return measure.result()


class PolygonGeometry(PolylineGeometry):
    def __init__(self, vertexes: Optional[List[Point]] = None, algorithm: Optional[LineAlgorithm] = None) -> None:
        super().__init__(vertexes, algorithm)

    def transformed(self) -> Geometry:
        if self.transform is None:
            return self
        else:
            vertexes = list(map(self.transform.transform, self.vertexes))
            return PolygonGeometry(vertexes, self.algorithm)

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        target = self
        if self.transform is not None:
            target = cast(PolygonGeometry, self.transformed())
        cnt = len(target.vertexes)
        if cnt > 0:
            for point in super(PolygonGeometry, target).strokePoints(pen):
                yield point
            ln = LineGeometry(target.vertexes[-1],
                              target.vertexes[0], target.algorithm)
            for point in ln.strokePoints(pen):
                yield point
