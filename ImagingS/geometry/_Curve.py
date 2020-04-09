from __future__ import annotations

from enum import Enum, unique
from typing import Iterable, Iterator, List

from ImagingS import Point
from ImagingS.drawing import Pen

from . import Geometry


@unique
class CurveAlgorithm(Enum):
    Bezier = 0
    BSpline = 1


def _calcPointCount(points: List[Point]) -> int:
    cnt = 0
    for i in range(len(points)-1):
        cnt += abs(points[i+1]-points[i])
    cnt = int(cnt) * 2
    return cnt


def _genBezier(points: List[Point]) -> Iterator[Point]:
    def casteljau(ps: List[Point], t: float) -> Point:
        cps = [p.clone() for p in ps]
        n = len(cps) - 1
        for i in range(1, n+1):
            for j in range(n-i+1):
                cps[j] = cps[j] + t * (cps[j+1] - cps[j])
        return cps[0]
    cnt = _calcPointCount(points)
    for t in range(cnt+1):
        p = casteljau(points, t / cnt)
        yield p


def _genBSpline3(points: List[Point]) -> Iterator[Point]:
    def subline(ps: List[Point]) -> Iterator[Point]:
        assert len(ps) == 4
        cnt = _calcPointCount(ps)
        for tc in range(cnt+1):
            t = tc / cnt
            t2 = t * t
            t3 = t2 * t
            f03 = (3*t2 - t3 - 3*t + 1) / 6
            f13 = (3*t3 - 6*t2 + 4) / 6
            f23 = (3*t2 - 3*t3 + 3*t + 1) / 6
            f33 = t3 / 6
            yield f03*ps[0] + f13*ps[1] + f23*ps[2] + f33*ps[3]
    for i in range(len(points)-3):
        for p in subline(points[i:i+4]):
            yield p


class CurveGeometry(Geometry):
    def __init__(self, ) -> None:
        super().__init__()
        self.controlPoints = []
        self.algorithm = CurveAlgorithm.Bezier

    @staticmethod
    def create(controlPoints: List[Point], algorithm: CurveAlgorithm) -> CurveGeometry:
        result = CurveGeometry()
        result.controlPoints = controlPoints
        result.algorithm = algorithm
        return result

    @property
    def controlPoints(self) -> List[Point]:
        return self._controlPoints

    @controlPoints.setter
    def controlPoints(self, value: List[Point]) -> None:
        self._controlPoints = value

    @property
    def algorithm(self) -> CurveAlgorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: CurveAlgorithm) -> None:
        self._algorithm = value

    def strokePoints(self, pen: Pen) -> Iterable[Point]:
        lp = self.controlPoints
        if self.transform is not None:
            lp = list(map(self.transform.transform, lp))
        gen = None
        if self.algorithm is CurveAlgorithm.Bezier:
            gen = _genBezier
        elif self.algorithm is CurveAlgorithm.BSpline:
            gen = _genBSpline3
        return gen(lp)

    def fillPoints(self) -> Iterable[Point]:
        return []
