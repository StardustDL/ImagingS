import math

import numpy as np

from ImagingS import Point, feq
from ImagingS.transform import (MatrixTransform, RotateTransform,
                                ScaleTransform, SkewTransform,
                                TranslateTransform)


def test_clip() -> None:
    pass


def test_matrix() -> None:
    tr = MatrixTransform(np.array([[1, 2, 0], [3, 4, 0], [0, 0, 1]]))
    assert tr.matrix[0][0] == 1
    assert Point(1, 3) == tr.transform(Point(1, 0))
    assert Point(2, 4) == tr.transform(Point(0, 1))


def test_rotate() -> None:
    tr = RotateTransform(Point(0, 0), math.pi / 2)
    assert Point(0, 0) == tr.center
    assert feq(tr.angle, math.pi / 2)
    assert Point(0, 1) == tr.transform(Point(1, 0))
    assert Point(-1, 0) == tr.transform(Point(0, 1))


def test_scale() -> None:
    tr = ScaleTransform(Point(0, 0), (2, 2))
    assert Point(0, 0) == tr.center
    assert (2, 2) == tr.factor
    assert Point(2, 0) == tr.transform(Point(1, 0))
    assert Point(0, 2) == tr.transform(Point(0, 1))


def test_skew() -> None:
    tr = SkewTransform(Point(0, 0), (math.pi / 4, 0))
    assert Point(0, 0) == tr.center
    assert feq(tr.angle[0], math.pi / 4)
    assert feq(tr.angle[1], 0)
    assert Point(1, 0) == tr.transform(Point(1, 0))
    assert Point(1, 1) == tr.transform(Point(0, 1))


def test_translate() -> None:
    tr = TranslateTransform(Point(1, 1))
    assert Point(1, 1) == tr.delta
    assert Point(2, 1) == tr.transform(Point(1, 0))
    assert Point(1, 2) == tr.transform(Point(0, 1))
