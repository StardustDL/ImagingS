from typing import cast
import numpy as np
from ImagingS.core import Point, RectArea, Size
from ImagingS.core.brush import Brushes, SolidBrush
from ImagingS.core.transform import TranslateTransform, SkewTransform, RotateTransform, MatrixTransform, ClipTransform, ScaleTransform, TransformGroup
from ImagingS.document import Document
from ImagingS.core.geometry import Line, Polygon, Curve, Ellipse
import os


def _get_parent_dir(path: str) -> str:
    return os.path.split(path)[0]


def _get_temp_dir() -> str:
    curdir = _get_parent_dir(_get_parent_dir(
        _get_parent_dir(os.path.realpath(__file__))))
    tempdir = os.path.join(curdir, "temp")
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)
    return tempdir


def test_sl() -> None:
    curdir = _get_temp_dir()
    doc = Document()
    doc.brushes.append(Brushes.Black())
    doc.brushes.append(Brushes.White())

    line = Line.create(Point.create(0, 0), Point.create(1, 1), "DDA")
    line.id = "line"
    line.transform = TranslateTransform()

    curve = Curve.create([Point.create(2, 2)], "alg")
    curve.id = "curve"
    curve.transform = SkewTransform.create(Point(), 1, 1)

    poly = Polygon.create([Point.create(2, 2)], "DDA")
    poly.id = "poly"
    poly.transform = RotateTransform.create(Point(), 3)

    ell = Ellipse.create(RectArea.create(Point(), Size.create(10, 10)))
    ell.id = "ell"
    tg = TransformGroup()
    tg.children.append(MatrixTransform.create(np.ones((2, 2))))
    tg.children.append(ScaleTransform.create(Point(), 2))
    tg.children.append(ClipTransform.create(
        RectArea.create(Point(), Size.create(10, 10)), "cli"))
    ell.transform = tg

    doc.drawings.append(line)
    doc.drawings.append(curve)
    doc.drawings.append(poly)
    doc.drawings.append(ell)

    file = os.path.join(curdir, "doc.json")
    with open(file, mode="w+") as f:
        doc.save(f)
    with open(file, mode="r") as f:
        docl = Document.load(f)

    assert len(docl.brushes) == 2
    assert isinstance(docl.brushes[0], SolidBrush)
    assert isinstance(docl.brushes[1], SolidBrush)
    assert cast(SolidBrush, docl.brushes[0]).color == cast(
        SolidBrush, doc.brushes[0]).color
    assert cast(SolidBrush, docl.brushes[1]).color == cast(
        SolidBrush, doc.brushes[1]).color
    assert cast(Line, docl.drawings["line"]).start == line.start
    assert cast(Line, docl.drawings["line"]).end == line.end
    assert cast(Line, docl.drawings["line"]).algorithm == line.algorithm
    assert cast(Curve, docl.drawings["curve"]).algorithm == curve.algorithm
    assert cast(Polygon, docl.drawings["poly"]).algorithm == poly.algorithm
    assert cast(Ellipse, docl.drawings["ell"]).area == ell.area
