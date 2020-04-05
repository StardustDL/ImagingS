from ImagingS.core.drawing import Drawing
from typing import Optional
import ImagingS.Gui.ui as ui
from ImagingS.Gui import icons
from ImagingS.core.brush import SolidBrush, Brush
from ImagingS.document import Document
from ImagingS.core.geometry import Line, Curve, Polygon, Ellipse, Geometry
from ImagingS.Gui.graphics import Canvas, converters
from ImagingS.core.transform import MatrixTransform, TransformGroup
from ImagingS.Gui.interactive import Interactive
from ImagingS.Gui.interactive.geometry import LineInteractive, PolygonInteractive, CurveInteractive, EllipseInteractive
from ImagingS.Gui.interactive.transform import TranslateTransformInteractive, SkewTransformInteractive, RotateTransformInteractive, ScaleTransformInteractive, ClipTransformInteractive
import uuid

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, QSizeF


class VisualPage(QWidget, ui.VisualPage):
    messaged = pyqtSignal(str)
    drawingCreated = pyqtSignal(Drawing)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupIcon()
        self.setupCanvas()

        self.actionDrawings = [
            self.actDrawingLine,
            self.actDrawingPolygon,
            self.actDrawingCurve,
            self.actDrawingEllipse,
        ]

        self.actionTransforms = [
            self.actTransformTranslate,
            self.actTransformScale,
            self.actTransformRotate,
            self.actTransformSkew,
            self.actTransformMatrix,
            self.actTransformClip,
        ]

        self.actDrawingCurve.triggered.connect(self.actDrawingCurve_triggered)
        self.actDrawingLine.triggered.connect(self.actDrawingLine_triggered)
        self.actDrawingEllipse.triggered.connect(
            self.actDrawingEllipse_triggered)
        self.actDrawingPolygon.triggered.connect(
            self.actDrawingPolygon_triggered)

        self.actTransformTranslate.triggered.connect(
            self.actTransformTranslate_triggered)
        self.actTransformSkew.triggered.connect(
            self.actTransformSkew_triggered)
        self.actTransformRotate.triggered.connect(
            self.actTransformRotate_triggered)
        self.actTransformMatrix.triggered.connect(
            self.actTransformMatrix_triggered)
        self.actTransformScale.triggered.connect(
            self.actTransformScale_triggered)
        self.actTransformClip.triggered.connect(
            self.actTransformClip_triggered)
        self.actTransformGroup.triggered.connect(
            self.actTransformGroup_triggered)

        self.interactive = None
        self.drawing = None
        self.brush = None
        self.document = None

    def setupIcon(self):
        self.actDrawingLine.setIcon(icons.line)
        self.actDrawingCurve.setIcon(icons.curve)
        self.actDrawingEllipse.setIcon(icons.ellipse)
        self.actDrawingPolygon.setIcon(icons.polygon)
        self.actTransformSkew.setIcon(icons.skewTransform)
        self.actTransformScale.setIcon(icons.scaleTransform)
        self.actTransformTranslate.setIcon(icons.translateTransform)
        self.actTransformRotate.setIcon(icons.rotateTransform)
        self.actTransformMatrix.setIcon(icons.matrixTransform)
        self.actTransformClip.setIcon(icons.clipTransform)
        self.actTransformGroup.setIcon(icons.groupTransform)

    def setupCanvas(self):
        self.gvwMain = Canvas(self.widMain)
        self.gvwMain.setObjectName("gvwMain")
        self.grdMain.addWidget(self.gvwMain, 0, 0, 1, 1)
        self.gvwMain.resize(QSizeF(600, 600))

    @property
    def document(self) -> Optional[Document]:
        return self._document

    @document.setter
    def document(self, value: Optional[Document]) -> None:
        self._document = value
        self.fresh()

    @property
    def drawing(self) -> Optional[Drawing]:
        return self._drawing

    @drawing.setter
    def drawing(self, value: Optional[Drawing]) -> None:
        self._drawing = value
        if value is not None:
            self.gvwMain.select(value.id)
            self.messaged.emit(f"Current drawing: {value.id}")
        else:
            self.gvwMain.select(None)
            self.messaged.emit("")

    @property
    def brush(self) -> Optional[Brush]:
        return self._brush

    @brush.setter
    def brush(self, value: Optional[Brush]) -> None:
        self._brush = value
        if value is not None:
            if isinstance(value, SolidBrush):
                self.messaged.emit(
                    f"Current brush: {value.color.to_hex()}")
        else:
            self.messaged.emit("")

    @property
    def interactive(self) -> Optional[Interactive]:
        return self._interactive

    @interactive.setter
    def interactive(self, value: Optional[Interactive]) -> None:
        self._interactive = value
        self.gvwMain.interactive = self._interactive

    def fresh(self) -> None:
        self.gvwMain.clear()
        self.drawing = None
        self.brush = None
        hasDoc = self.document is not None

        for act in self.actionDrawings:
            act.setEnabled(hasDoc)
        for act in self.actionTransforms:
            act.setEnabled(hasDoc)

        self.gvwMain.setEnabled(hasDoc)
        self.tlbMain.setEnabled(hasDoc)

        if hasDoc:
            self.gvwMain.resize(converters.convert_size(self.document.size))
            for br in self.document.drawings:
                self.gvwMain.add(br)

    def resetDrawingActionChecked(self, checkedAction=None):
        for act in self.actionDrawings:
            if act.isCheckable() and act is not checkedAction:
                act.setChecked(False)

    def _create_geometry(self, geo: Geometry) -> None:
        brush = self.brush
        if brush is not None:
            geo.stroke = brush
        self.gvwMain.add(geo)

    def interDrawing_ended(self) -> None:
        if self.interactive is None:
            return
        inter = self.interactive
        drawing: Optional[Drawing] = None
        if isinstance(inter, LineInteractive):
            drawing = inter.drawing
            self.actDrawingLine.trigger()
        elif isinstance(inter, PolygonInteractive):
            drawing = inter.drawing
            self.actDrawingPolygon.trigger()
        elif isinstance(inter, CurveInteractive):
            drawing = inter.drawing
            self.actDrawingCurve.trigger()
        elif isinstance(inter, EllipseInteractive):
            drawing = inter.drawing
            self.actDrawingEllipse.trigger()
        if drawing is None:
            return
        if inter.state == Interactive.S_Success:
            self.document.drawings.append(drawing)
            self.drawingCreated.emit(drawing)
            self.drawing = drawing
        else:
            self.gvwMain.remove(inter.drawing.id)
        self.interactive = None

    def interTransform_ended(self) -> None:
        if self.interactive is None:
            return
        inter = self.interactive
        drawing = self.drawing
        if drawing is None:
            return
        drawing.refresh_boundingArea()
        if inter.state == Interactive.S_Success:
            pass
        else:
            drawing.transform = None
        self.gvwMain.rerender()
        self.interactive = None

    def actDrawingCurve_triggered(self):
        if not self.actDrawingCurve.isChecked():
            self.interactive = None
            return
        self.resetDrawingActionChecked(self.actDrawingCurve)
        curve = Curve()
        curve.id = str(uuid.uuid1())
        self._create_geometry(curve)
        inter = CurveInteractive(curve)
        inter.ended.connect(self.interDrawing_ended)
        self.interactive = inter

    def actDrawingPolygon_triggered(self):
        if not self.actDrawingPolygon.isChecked():
            self.interactive = None
            return
        self.resetDrawingActionChecked(self.actDrawingPolygon)
        polygon = Polygon()
        polygon.id = str(uuid.uuid1())
        self._create_geometry(polygon)
        inter = PolygonInteractive(polygon)
        inter.ended.connect(self.interDrawing_ended)
        self.interactive = inter

    def actDrawingEllipse_triggered(self):
        if not self.actDrawingEllipse.isChecked():
            self.interactive = None
            return
        self.resetDrawingActionChecked(self.actDrawingEllipse)
        ell = Ellipse()
        ell.id = str(uuid.uuid1())
        self._create_geometry(ell)
        inter = EllipseInteractive(ell)
        inter.ended.connect(self.interDrawing_ended)
        self.interactive = inter

    def actDrawingLine_triggered(self):
        if not self.actDrawingLine.isChecked():
            self.interactive = None
            return
        self.resetDrawingActionChecked(self.actDrawingLine)
        line = Line()
        line.id = str(uuid.uuid1())
        self._create_geometry(line)
        inter = LineInteractive(line)
        inter.ended.connect(self.interDrawing_ended)
        self.interactive = inter

    def actTransformTranslate_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        inter = TranslateTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self.interactive = inter

    def actTransformSkew_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        inter = SkewTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self.interactive = inter

    def actTransformRotate_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        inter = RotateTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self.interactive = inter

    def actTransformMatrix_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        drawing.transform = MatrixTransform()

    def actTransformScale_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        inter = ScaleTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self.interactive = inter

    def actTransformClip_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        inter = ClipTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self.interactive = inter

    def actTransformGroup_triggered(self):
        drawing = self.drawing
        if drawing is None:
            return
        drawing.transform = TransformGroup()
        self.gvwMain.rerender()
