import os
from test.temp import get_temp_dir
from typing import cast

import numpy as np

from ImagingS import Point, Rect, Size
from ImagingS.brush import Brushes, SolidBrush
from ImagingS.document import Document, DocumentFormat
from ImagingS.drawing import GeometryDrawing
from ImagingS.geometry import (CurveAlgorithm, CurveGeometry, EllipseGeometry,
                               LineAlgorithm, LineGeometry, PolygonGeometry)
from ImagingS.transform import (MatrixTransform, RotateTransform,
                                ScaleTransform, SkewTransform, TransformGroup,
                                TranslateTransform)


def test_saveload() -> None:
    curdir = get_temp_dir()
    doc = Document()
    doc.brushes.append(Brushes.Black)
    doc.brushes.append(Brushes.White)

    lineG = LineGeometry.create(Point.create(
        0, 0), Point.create(1, 1), LineAlgorithm.Dda)
    lineG.transform = TranslateTransform()
    line = GeometryDrawing.create(lineG)
    line.id = "line"

    curveG = CurveGeometry.create([Point.create(2, 2)], CurveAlgorithm.Bezier)
    curveG.transform = SkewTransform.create(Point(), (1, 1))
    curve = GeometryDrawing.create(curveG)
    curve.id = "curve"

    polyG = PolygonGeometry.create([Point.create(2, 2)], LineAlgorithm.Dda)
    polyG.transform = RotateTransform.create(Point(), 3)
    poly = GeometryDrawing.create(polyG)
    poly.id = "poly"

    ellG = EllipseGeometry.fromRect(Rect.create(Point(), Size.create(10, 10)))
    tg = TransformGroup()
    tg.children.append(MatrixTransform.create(np.ones((3, 3))))
    tg.children.append(ScaleTransform.create(Point(), (2, 2)))
    ellG.transform = tg
    ell = GeometryDrawing.create(ellG)
    ell.id = "ell"

    doc.drawings.children.append(line)
    doc.drawings.children.append(curve)
    doc.drawings.children.append(poly)
    doc.drawings.children.append(ell)

    def check(docl: Document) -> None:
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
                                          docl.drawings.children["ell"]).geometry).center == ellG.center

    file = os.path.join(curdir, "doc.json")
    with open(file, mode="w+") as f:
        doc.save(f, DocumentFormat.RAW)
    with open(file, mode="r") as f:
        docl = Document.load(f, DocumentFormat.RAW)
    check(docl)

    file = os.path.join(curdir, "doc.isd")
    with open(file, mode="wb") as f:
        doc.save(f)
    with open(file, mode="rb") as f:
        docl = Document.load(f)
    check(docl)
