from ImagingS.core.brush import Brushes, SolidBrush
from ImagingS.core.geometry import Line, Polygon, Curve, Ellipse
from ImagingS.core.transform import TranslateTransform, RotateTransform, ClipTransform, ScaleTransform
from typing import List
from ImagingS.core import RectArea, Size, Color, Point
from ImagingS.document import Document
import math
import os


class BuiltinInstruction:
    def __init__(self, doc: Document, output_dir: str) -> None:
        self.doc = doc
        self.brush = Brushes.Black()
        self.output_dir = output_dir

    def resetCanvas(self, argv: List[str]) -> None:
        self.doc.size = Size.create(int(argv[0]), int(argv[1]))

    def saveCanvas(self, argv: List[str]) -> None:
        with open(os.path.join(self.output_dir, f"{argv[0]}.isd.json"), "w+") as f:
            self.doc.save(f)

    def setColor(self, argv: List[str]) -> None:
        self.brush = SolidBrush.create(
            Color.create(int(argv[0]), int(argv[1]), int(argv[2])))

    def drawLine(self, argv: List[str]) -> None:
        drawing = Line.create(Point.create(int(argv[1]), int(argv[2])), Point.create(
            int(argv[3]), int(argv[4])), argv[5])
        drawing.id = argv[0]
        drawing.stroke = self.brush
        self.doc.drawings.append(drawing)

    def drawPolygon(self, argv: List[str]) -> None:
        vers: List[Point] = []
        ps = argv[1:-1]
        i = 0
        while i < len(ps):
            vers.append(Point.create(int(ps[i]), int(ps[i+1])))
            i += 2
        drawing = Polygon.create(vers, argv[-1])
        drawing.id = argv[0]
        drawing.stroke = self.brush
        self.doc.drawings.append(drawing)

    def drawEllipse(self, argv: List[str]) -> None:
        lt = Point.create(int(argv[1]), int(argv[2]))
        rb = Point.create(int(argv[3]), int(argv[4]))
        delta = rb - lt
        drawing = Ellipse.create(RectArea.create(
            lt, Size.create(delta.x, delta.y)))
        drawing.id = argv[0]
        drawing.stroke = self.brush
        self.doc.drawings.append(drawing)

    def drawCurve(self, argv: List[str]) -> None:
        vers: List[Point] = []
        ps = argv[1:-1]
        i = 0
        while i < len(ps):
            vers.append(Point.create(int(ps[i]), int(ps[i+1])))
            i += 2
        drawing = Curve.create(vers, argv[-1])
        drawing.id = argv[0]
        drawing.stroke = self.brush
        self.doc.drawings.append(drawing)

    def translate(self, argv: List[str]) -> None:
        drawing = self.doc.drawings[argv[0]]
        drawing.transform = TranslateTransform.create(
            Point.create(int(argv[1]), int(argv[2])))

    def rotate(self, argv: List[str]) -> None:
        drawing = self.doc.drawings[argv[0]]
        drawing.transform = RotateTransform.create(
            Point.create(int(argv[1]), int(argv[2])), int(argv[3]) / 360 * 2 * math.pi)

    def scale(self, argv: List[str]) -> None:
        drawing = self.doc.drawings[argv[0]]
        drawing.transform = ScaleTransform.create(
            Point.create(int(argv[1]), int(argv[2])), int(argv[3]))

    def clip(self, argv: List[str]) -> None:
        drawing = self.doc.drawings[argv[0]]
        lt = Point.create(int(argv[1]), int(argv[2]))
        rb = Point.create(int(argv[3]), int(argv[4]))
        delta = rb - lt
        trans = ClipTransform.create(RectArea.create(
            lt, Size.create(delta.x, delta.y)), argv[5])
        drawing.transform = trans

    def execute(self, ins: str) -> None:
        ins = ins.strip()
        if not ins:
            return
        items = ins.split(" ")
        m = getattr(self, items[0])
        m.__call__(items[1:])
