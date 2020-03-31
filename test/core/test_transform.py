from ImagingS.core import Point
from ImagingS.core.transform import Matrix, Translate, Rotate, Scale
import math
import numpy as np


def test_Clip() -> None:
    pass


def test_Matrix() -> None:
    tr = Matrix(np.array([[1, 2], [3, 4]]))
    assert Point(1, 3) == tr.transform(Point(1, 0))
    assert Point(2, 4) == tr.transform(Point(0, 1))


def test_Rotate() -> None:
    tr = Rotate(Point(0, 0), math.pi / 2)
    assert Point(0, 1) == tr.transform(Point(1, 0))
    assert Point(-1, 0) == tr.transform(Point(0, 1))


def test_Scale() -> None:
    tr = Scale(Point(0, 0), 2)
    assert Point(2, 0) == tr.transform(Point(1, 0))
    assert Point(0, 2) == tr.transform(Point(0, 1))


def test_Skew() -> None:
    pass


def test_Translate() -> None:
    tr = Translate(Point(1, 1))
    assert Point(2, 1) == tr.transform(Point(1, 0))
    assert Point(1, 2) == tr.transform(Point(0, 1))
