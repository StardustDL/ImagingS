import os
from test.temp import get_temp_dir
from typing import cast

import numpy as np

from ImagingS.core import Point, Rect, Size
from ImagingS.core.brush import Brushes, SolidBrush
from ImagingS.core.drawing import GeometryDrawing
from ImagingS.core.geometry import (CurveGeometry, EllipseGeometry,
                                    LineGeometry, PolygonGeometry)
from ImagingS.core.transform import (MatrixTransform, RotateTransform,
                                     ScaleTransform, SkewTransform,
                                     TransformGroup, TranslateTransform)
from ImagingS.document import Document


def test_sl() -> None:
    curdir = get_temp_dir()
    doc = Document()
    doc.brushes.append(Brushes.Black())
    doc.brushes.append(Brushes.White())

    lineG = LineGeometry.create(Point.create(0, 0), Point.create(1, 1), "DDA")
    lineG.transform = TranslateTransform()
    line = GeometryDrawing.create(lineG)
    line.id = "line"

    curveG = CurveGeometry.create([Point.create(2, 2)], "alg")
    curveG.transform = SkewTransform.create(Point(), 1, 1)
    curve = GeometryDrawing.create(curveG)
    curve.id = "curve"

    polyG = PolygonGeometry.create([Point.create(2, 2)], "DDA")
    polyG.transform = RotateTransform.create(Point(), 3)
    poly = GeometryDrawing.create(polyG)
    poly.id = "poly"

    ellG = EllipseGeometry.create(Rect.create(Point(), Size.create(10, 10)))
    tg = TransformGroup()
    tg.children.append(MatrixTransform.create(np.ones((2, 2))))
    tg.children.append(ScaleTransform.create(Point(), 2))
    ellG.transform = tg
    ell = GeometryDrawing.create(ellG)
    ell.id = "ell"

    doc.drawings.children.append(line)
    doc.drawings.children.append(curve)
    doc.drawings.children.append(poly)
    doc.drawings.children.append(ell)

    file = os.path.join(curdir, "doc.json")
    with open(file, mode="wb") as f:
        doc.save(f)
    with open(file, mode="rb") as f:
        docl = Document.load(f)

    assert len(docl.brushes) == 2
    assert isinstance(docl.brushes[0], SolidBrush)
    assert isinstance(docl.brushes[1], SolidBrush)
    assert cast(SolidBrush, docl.brushes[0]).color == cast(
        SolidBrush, doc.brushes[0]).color
    assert cast(SolidBrush, docl.brushes[1]).color == cast(
        SolidBrush, doc.brushes[1]).color
    assert isinstance(docl.drawings.children["line"], GeometryDrawing)
    assert cast(LineGeometry, cast(GeometryDrawing,
                                   docl.drawings.children["line"]).geometry).start == lineG.start
    assert cast(LineGeometry, cast(GeometryDrawing,
                                   docl.drawings.children["line"]).geometry).end == lineG.end
    assert cast(LineGeometry, cast(GeometryDrawing,
                                   docl.drawings.children["line"]).geometry).algorithm == lineG.algorithm
    assert cast(CurveGeometry, cast(GeometryDrawing,
                                    docl.drawings.children["curve"]).geometry).algorithm == curveG.algorithm
    assert cast(PolygonGeometry, cast(GeometryDrawing,
                                      docl.drawings.children["poly"]).geometry).algorithm == polyG.algorithm
    assert cast(EllipseGeometry, cast(GeometryDrawing,
                                      docl.drawings.children["ell"]).geometry).area == ellG.area
