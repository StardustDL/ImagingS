from ImagingS.core import Point
from ImagingS.core.transform import MatrixTransform, TranslateTransform, RotateTransform, ScaleTransform, SkewTransform
import math
import numpy as np


def test_Clip() -> None:
    pass


def test_Matrix() -> None:
    tr = MatrixTransform(np.array([[1, 2], [3, 4]]))
    assert tr.matrix[0][0] == 1
    assert Point(1, 3) == tr.transform(Point(1, 0))
    assert Point(2, 4) == tr.transform(Point(0, 1))


def test_Rotate() -> None:
    tr = RotateTransform(Point(0, 0), math.pi / 2)
    assert Point(0, 0) == tr.center
    assert math.fabs(tr.angle - math.pi / 2) < 1e-8
    assert Point(0, 1) == tr.transform(Point(1, 0))
    assert Point(-1, 0) == tr.transform(Point(0, 1))


def test_Scale() -> None:
    tr = ScaleTransform(Point(0, 0), 2)
    assert Point(0, 0) == tr.center
    assert 2 == tr.factor
    assert Point(2, 0) == tr.transform(Point(1, 0))
    assert Point(0, 2) == tr.transform(Point(0, 1))


def test_Skew() -> None:
    tr = SkewTransform(Point(0, 0), math.pi / 4, 0)
    assert Point(0, 0) == tr.center
    assert math.fabs(tr.angle_x - math.pi / 4) < 1e-8
    assert math.fabs(tr.angle_y - 0) < 1e-8
    assert Point(1, 0) == tr.transform(Point(1, 0))
    assert Point(2**0.5 / 2, 2**0.5 / 2) == tr.transform(Point(0, 1))


def test_Translate() -> None:
    tr = TranslateTransform(Point(1, 1))
    assert Point(1, 1) == tr.delta
    assert Point(2, 1) == tr.transform(Point(1, 0))
    assert Point(1, 2) == tr.transform(Point(0, 1))
