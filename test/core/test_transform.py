import math

import numpy as np

from ImagingS import Point
from ImagingS.transform import (MatrixTransform, RotateTransform,
                                ScaleTransform, SkewTransform,
                                TranslateTransform)


def test_Clip() -> None:
    pass


def test_Matrix() -> None:
    tr = MatrixTransform.create(np.array([[1, 2], [3, 4]]))
    assert tr.matrix[0][0] == 1
    assert Point.create(1, 3) == tr.transform(Point.create(1, 0))
    assert Point.create(2, 4) == tr.transform(Point.create(0, 1))


def test_Rotate() -> None:
    tr = RotateTransform.create(Point.create(0, 0), math.pi / 2)
    assert Point.create(0, 0) == tr.center
    assert math.fabs(tr.angle - math.pi / 2) < 1e-8
    assert Point.create(0, 1) == tr.transform(Point.create(1, 0))
    assert Point.create(-1, 0) == tr.transform(Point.create(0, 1))


def test_Scale() -> None:
    tr = ScaleTransform.create(Point.create(0, 0), 2)
    assert Point.create(0, 0) == tr.center
    assert 2 == tr.factor
    assert Point.create(2, 0) == tr.transform(Point.create(1, 0))
    assert Point.create(0, 2) == tr.transform(Point.create(0, 1))


def test_Skew() -> None:
    tr = SkewTransform.create(Point.create(0, 0), math.pi / 4, 0)
    assert Point.create(0, 0) == tr.center
    assert math.fabs(tr.angle_x - math.pi / 4) < 1e-8
    assert math.fabs(tr.angle_y - 0) < 1e-8
    assert Point.create(1, 0) == tr.transform(Point.create(1, 0))
    assert Point.create(1, 1) == tr.transform(Point.create(0, 1))


def test_Translate() -> None:
    tr = TranslateTransform.create(Point.create(1, 1))
    assert Point.create(1, 1) == tr.delta
    assert Point.create(2, 1) == tr.transform(Point.create(1, 0))
    assert Point.create(1, 2) == tr.transform(Point.create(0, 1))
