import math
import os
from typing import List

from PIL import Image

from ImagingS import Color, Point, Rect, Size
from ImagingS.brush import Brushes, SolidBrush
from ImagingS.document import Document
from ImagingS.drawing import GeometryDrawing, NumpyArrayDrawingContext, Pen
from ImagingS.geometry import (CurveAlgorithm, CurveGeometry, EllipseGeometry,
                               LineAlgorithm, LineClipAlgorithm, LineGeometry,
                               PolygonGeometry)
from ImagingS.transform import (RotateTransform, ScaleTransform, Transform,
                                TransformGroup, TranslateTransform)


def _append_transform(drawing: GeometryDrawing, transform: Transform) -> None:
    assert not isinstance(transform, TransformGroup)
    geometry = drawing.geometry
    if geometry.transform is None:
        geometry.transform = transform
    elif isinstance(geometry.transform, TransformGroup):
        geometry.transform.children.append(transform)
    else:
        old = geometry.transform
        new = TransformGroup()
        new.children.append(old)
        new.children.append(transform)
        geometry.transform = new


class BuiltinInstruction:
    def __init__(self, doc: Document, output_dir: str) -> None:
        self.doc = doc
        self.brush = Brushes.Black
        self.output_dir = output_dir

    def resetCanvas(self, argv: List[str]) -> None:
        self.doc.size = Size.create(int(argv[0]), int(argv[1]))
        self.doc.drawings.children.clear()

    def saveCanvas(self, argv: List[str]) -> None:
        fileName = os.path.join(self.output_dir, f"{argv[0]}.bmp")

        context = NumpyArrayDrawingContext(
            NumpyArrayDrawingContext.create_array(self.doc.size))

        self.doc.drawings.render(context)

        Image.fromarray(context.array).save(fileName, "bmp")

    def setColor(self, argv: List[str]) -> None:
        self.brush = SolidBrush.create(
            Color.create(int(argv[0]), int(argv[1]), int(argv[2])))

    def drawLine(self, argv: List[str]) -> None:
        geometry = LineGeometry.create(Point.create(int(argv[1]), int(argv[2])), Point.create(
            int(argv[3]), int(argv[4])), LineAlgorithm.Dda if argv[5] == "DDA" else LineAlgorithm.Bresenham)
        drawing = GeometryDrawing.create(geometry)
        drawing.id = argv[0]
        drawing.stroke = Pen.create(self.brush)
        self.doc.drawings.children.append(drawing)

    def drawPolygon(self, argv: List[str]) -> None:
        vers: List[Point] = []
        ps = argv[1:-1]
        i = 0
        while i < len(ps):
            vers.append(Point.create(int(ps[i]), int(ps[i+1])))
            i += 2
        geometry = PolygonGeometry.create(
            vers, LineAlgorithm.Dda if argv[-1] == "DDA" else LineAlgorithm.Bresenham)
        drawing = GeometryDrawing.create(geometry)
        drawing.id = argv[0]
        drawing.stroke = Pen.create(self.brush)
        self.doc.drawings.children.append(drawing)

    def drawEllipse(self, argv: List[str]) -> None:
        lt = Point.create(int(argv[1]), int(argv[2]))
        rb = Point.create(int(argv[3]), int(argv[4]))
        geometry = EllipseGeometry.create(Rect.from_points(lt, rb))
        drawing = GeometryDrawing.create(geometry)
        drawing.id = argv[0]
        drawing.stroke = Pen.create(self.brush)
        self.doc.drawings.children.append(drawing)

    def drawCurve(self, argv: List[str]) -> None:
        vers: List[Point] = []
        ps = argv[1:-1]
        i = 0
        while i < len(ps):
            vers.append(Point.create(int(ps[i]), int(ps[i+1])))
            i += 2
        geometry = CurveGeometry.create(
            vers, CurveAlgorithm.Bezier if argv[-1] == "Bezier" else CurveAlgorithm.BSpline)
        drawing = GeometryDrawing.create(geometry)
        drawing.id = argv[0]
        drawing.stroke = Pen.create(self.brush)
        self.doc.drawings.children.append(drawing)

    def translate(self, argv: List[str]) -> None:
        drawing = self.doc.drawings.children[argv[0]]
        assert isinstance(drawing, GeometryDrawing)
        _append_transform(drawing, TranslateTransform.create(
            Point.create(int(argv[1]), int(argv[2]))))

    def rotate(self, argv: List[str]) -> None:
        drawing = self.doc.drawings.children[argv[0]]
        assert isinstance(drawing, GeometryDrawing)
        _append_transform(drawing, RotateTransform.create(
            Point.create(int(argv[1]), int(argv[2])), int(argv[3]) / 360 * 2 * math.pi))

    def scale(self, argv: List[str]) -> None:
        drawing = self.doc.drawings.children[argv[0]]
        assert isinstance(drawing, GeometryDrawing)
        _append_transform(drawing, ScaleTransform.create(
            Point.create(int(argv[1]), int(argv[2])), (int(argv[3]), int(argv[3]))))

    def clip(self, argv: List[str]) -> None:
        drawing = self.doc.drawings.children[argv[0]]
        assert isinstance(drawing, GeometryDrawing)
        assert isinstance(drawing.geometry, LineGeometry)
        lt = Point.create(int(argv[1]), int(argv[2]))
        rb = Point.create(int(argv[3]), int(argv[4]))
        drawing.geometry.clip = Rect.from_points(lt, rb)
        drawing.geometry.clip_algorithm = LineClipAlgorithm.CohenSutherland if argv[
            5] == "Cohen-Sutherland" else LineClipAlgorithm.LiangBarsky

    def execute(self, ins: str) -> None:
        ins = ins.strip()
        if not ins:
            return
        items = ins.split(" ")
        m = getattr(self, items[0])
        m.__call__(items[1:])
