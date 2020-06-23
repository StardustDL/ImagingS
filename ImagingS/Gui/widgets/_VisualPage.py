from enum import Enum, unique
from typing import Any, Dict, Optional, Tuple, Union, cast

from PyQt5.QtCore import QPointF, QSizeF, pyqtSignal
from PyQt5.QtWidgets import QInputDialog, QWidget

import ImagingS.Gui.ui as ui
from ImagingS.brush import Brush
from ImagingS.document import Document
from ImagingS.drawing import Drawing, DrawingGroup, GeometryDrawing, Pen
from ImagingS.geometry import (CurveAlgorithm, CurveGeometry, EllipseGeometry,
                               Geometry, LineAlgorithm, LineGeometry,
                               LineClipAlgorithm, LineClipper,
                               PolygonGeometry, PolylineGeometry,
                               RectangleGeometry)
from ImagingS.Gui import converters, icons
from ImagingS.Gui.graphic import Canvas
from ImagingS.Gui.interactivity import Interactivity, InteractivityState, RectClipInteractivity
from ImagingS.Gui.interactivity.geometry import (CurveInteractivity,
                                                 EllipseInteractivity,
                                                 GeometryInteractivity,
                                                 LineInteractivity,
                                                 PolylineInteractivity,
                                                 RectangleInteractivity)
from ImagingS.Gui.interactivity.transform import (
    RotateTransformInteractivity, ScaleTransformInteractivity,
    SkewTransformInteractivity, TransformInteractivity,
    TranslateTransformInteractivity)
from ImagingS.transform import (MatrixTransform, RotateTransform,
                                ScaleTransform, SkewTransform, TransformGroup,
                                TranslateTransform)

_TransformInteractiveCreateMap: Dict[str, Tuple[Any, Any]] = {
    "Translate": (TranslateTransform, TranslateTransformInteractivity),
    "Rotate": (RotateTransform, RotateTransformInteractivity),
    "Scale": (ScaleTransform, ScaleTransformInteractivity),
    "Skew": (SkewTransform, SkewTransformInteractivity),
}


@unique
class VisualPageState(Enum):
    Disable = 0
    Normal = 1
    Interactive = 2


class VisualPage(QWidget, ui.VisualPage):
    messaged = pyqtSignal(str)
    documentCommitted = pyqtSignal(Document, str)
    stateChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupToolBar()
        self.setupIcon()
        self.setupCanvas()

        # self.actionDrawings = [
        #     self.actDrawingLine,
        #     self.actDrawingPolygon,
        #     self.actDrawingCurve,
        #     self.actDrawingEllipse,
        # ]

        for act in [self.actTransformTranslate,
                    self.actTransformScale,
                    self.actTransformRotate,
                    self.actTransformSkew]:
            act.triggered.connect(self.actTransformCreate_triggered)

        self.actTransformMatrix.triggered.connect(self.actTransformMatrix_triggered)
        self.actTransformGroup.triggered.connect(self.actTransformGroup_triggered)

        self.actDrawingLine.triggered.connect(
            self.actDrawingLine_triggered)
        self.actDrawingPolygon.triggered.connect(
            self.actDrawingPolygon_triggered)
        self.actDrawingPolyline.triggered.connect(
            self.actDrawingPolyline_triggered)
        self.actDrawingRectangle.triggered.connect(
            self.actDrawingRectangle_triggered)
        self.actDrawingCurve.triggered.connect(
            self.actDrawingCurve_triggered)
        self.actDrawingEllipse.triggered.connect(
            self.actDrawingEllipse_triggered)

        self.actClip.triggered.connect(self.actClip_triggered)

        self.setEnabled(False)
        self._drawing = None
        self._state = VisualPageState.Disable

    def setupToolBar(self):
        # tb = QToolButton()
        # tb.setDefaultAction(self.actDrawingLine)
        # tb.setPopupMode(QToolButton.DelayedPopup)
        # self.tlbMain.addWidget(tb)

        # tb = QToolButton()
        # menu = QMenu()
        # menu.addActions([self.actDrawingPolygon,
        #                  self.actDrawingPolyline,
        #                  self.actDrawingRectangle])
        # tb.setDefaultAction(self.actDrawingPolygon)
        # tb.setMenu(menu)
        # tb.setPopupMode(QToolButton.DelayedPopup)
        # self.tlbMain.addWidget(tb)

        # tb = QToolButton()
        # tb.setDefaultAction(self.actDrawingCurve)
        # tb.setPopupMode(QToolButton.DelayedPopup)
        # self.tlbMain.addWidget(tb)

        # tb = QToolButton()
        # tb.setDefaultAction(self.actDrawingEllipse)
        # self.tlbMain.addWidget(tb)

        # self.tlbMain.addSeparator()

        # self.tlbMain.addActions([
        #     self.actTransformTranslate,
        #     self.actTransformScale,
        #     self.actTransformRotate,
        #     self.actTransformSkew,
        #     self.actTransformMatrix,
        #     self.actTransformGroup,
        # ])
        pass

    def setupIcon(self):
        self.actDrawingLine.setIcon(icons.lineGeometry)
        self.actDrawingCurve.setIcon(icons.curveGeometry)
        self.actDrawingEllipse.setIcon(icons.ellipseGeometry)
        self.actDrawingPolygon.setIcon(icons.polygonGeometry)
        self.actDrawingPolyline.setIcon(icons.polylineGeometry)
        self.actDrawingRectangle.setIcon(icons.rectangleGeometry)
        self.actTransformSkew.setIcon(icons.skewTransform)
        self.actTransformScale.setIcon(icons.scaleTransform)
        self.actTransformTranslate.setIcon(icons.translateTransform)
        self.actTransformRotate.setIcon(icons.rotateTransform)
        self.actTransformMatrix.setIcon(icons.matrixTransform)
        self.actTransformGroup.setIcon(icons.transformGroup)
        self.actClip.setIcon(icons.clip)

    def setupCanvas(self):
        self.cvsMain = Canvas(self.widMain)
        self.cvsMain.setObjectName("cvsMain")
        self.grdMain.addWidget(self.cvsMain, 0, 0, 1, 1)
        self.cvsMain.resize(QSizeF(600, 600))
        self.cvsMain.mouseMoved.connect(
            self.cvsMain_mouseMoved)
        self.cvsMain.mouseReleased.connect(
            self.cvsMain_mouseReleased)

    def enable(self, doc: Document) -> None:
        assert self.state is VisualPageState.Disable
        self.setEnabled(True)
        self._document = doc
        self.drawing = None
        self.brush = None
        self._setState(VisualPageState.Normal)
        self.fresh()

    def disable(self) -> None:
        assert self.state is not VisualPageState.Disable
        if hasattr(self, "_document"):
            del self._document
        self.drawing = None
        self.brush = None
        self.cvsMain.clear()
        self.setEnabled(False)
        self._setState(VisualPageState.Disable)

    def _setState(self, value: VisualPageState) -> None:
        self._state = value

        if self._state is VisualPageState.Interactive:
            self.tlbMain.setEnabled(False)
        elif self._state is VisualPageState.Normal:
            self.tlbMain.setEnabled(True)

        self.stateChanged.emit()

    @property
    def state(self) -> VisualPageState:
        return self._state

    @property
    def drawing(self) -> Optional[Drawing]:
        return self._drawing

    @drawing.setter
    def drawing(self, value: Optional[Drawing]) -> None:
        self._drawing = value
        if self.state is VisualPageState.Normal:
            self.cvsMain.select(
                self._drawing.id if self._drawing is not None else None)

    @property
    def brush(self) -> Optional[Brush]:
        return self._brush

    @brush.setter
    def brush(self, value: Optional[Brush]) -> None:
        self._brush = value

    def fresh(self) -> None:
        if self.state is not VisualPageState.Normal:
            return

        self.cvsMain.clear()
        self.cvsMain.resize(converters.qsize(self._document.size))
        for dr in self._document.drawings.children:
            self.cvsMain.add(dr)

    def cvsMain_mouseMoved(self, point: QPointF):
        self.messaged.emit(str((round(point.x()), round(point.y()))))

    def cvsMain_mouseReleased(self, point: QPointF):
        if self.state is VisualPageState.Normal:
            p = converters.point(point)
            for dr in reversed(self._document.drawings.children.items):
                if p in dr.bounds:
                    self.drawing = dr
                    break

    def _emptyGeometryDrawing(self) -> GeometryDrawing:
        drawing = GeometryDrawing()
        if self.brush is not None:
            drawing.stroke = Pen(self.brush)
        return drawing

    def _beginInteractive(self, inter: Interactivity) -> None:
        inter.ended.connect(self.interactivity_ended)
        inter.started.connect(self.interactivity_started)
        inter.updated.connect(self.interactivity_updated)
        self.cvsMain.interactivity = inter
        inter.start()

    def interactivity_started(self, inter: Interactivity) -> None:
        self._setState(VisualPageState.Interactive)
        if inter.viewItem is not None:
            self.cvsMain.scene().addItem(inter.viewItem)
        self.cvsMain.rerender()

    def interactivity_updated(self, inter: Interactivity) -> None:
        self.cvsMain.rerender()

    def interactivity_ended(self, inter: Interactivity) -> None:
        self._setState(VisualPageState.Normal)
        if inter.viewItem is not None:
            self.cvsMain.scene().removeItem(inter.viewItem)
        self.cvsMain.interactivity = None
        if inter.state is InteractivityState.Success:
            if isinstance(inter, GeometryInteractivity):
                drawing = cast(GeometryInteractivity, inter).target
                self._document.drawings.children.append(drawing)
                self.documentCommitted.emit(
                    self._document, f"Create {inter.geometry.__class__.__name__}")
            elif isinstance(inter, TransformInteractivity):
                if self.drawing is not None:
                    self.documentCommitted.emit(
                        self._document, f"Create {inter.transform.__class__.__name__}")
            elif isinstance(inter, RectClipInteractivity):
                if self.drawing is not None:
                    if isinstance(self.drawing, GeometryDrawing) and isinstance(self.drawing.geometry, LineGeometry):
                        drawingId = self.drawing.id

                        geo = self.drawing.geometry
                        clipper = LineClipper(cast(LineGeometry, geo.transformed()))
                        clipped = None
                        if inter.clip is not None:
                            clipped = clipper.clip(inter.clip, inter.clipAlgorithm)

                        if clipped is None:
                            parent = self.drawing.parent()
                            if parent is None:
                                return
                            del parent[drawingId]
                        else:
                            geo.start = clipped.start
                            geo.end = clipped.end
                            geo.transform = None  # clear transform

                        self.documentCommitted.emit(
                            self._document, f"Clip {drawingId}")
        self.fresh()

    def actDrawingLine_triggered(self):
        algs = [e.name for e in LineAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        geo = LineGeometry()
        geo.algorithm = getattr(LineAlgorithm, item)
        self._beginInteractive(LineInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actDrawingPolygon_triggered(self):
        algs = [e.name for e in LineAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        geo = PolygonGeometry()
        geo.algorithm = getattr(LineAlgorithm, item)
        self._beginInteractive(PolylineInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actDrawingPolyline_triggered(self):
        algs = [e.name for e in LineAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        geo = PolylineGeometry()
        geo.algorithm = getattr(LineAlgorithm, item)
        self._beginInteractive(PolylineInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actDrawingRectangle_triggered(self):
        algs = [e.name for e in LineAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        geo = RectangleGeometry()
        geo.algorithm = getattr(LineAlgorithm, item)
        self._beginInteractive(RectangleInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actDrawingCurve_triggered(self):
        algs = [e.name for e in CurveAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        geo = CurveGeometry()
        geo.algorithm = getattr(CurveAlgorithm, item)
        self._beginInteractive(CurveInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actDrawingEllipse_triggered(self):
        geo = EllipseGeometry()
        self._beginInteractive(EllipseInteractivity(
            self._emptyGeometryDrawing(), geo, self._document.size))

    def actClip_triggered(self):
        if self.drawing is None:
            return
        target = None
        if isinstance(self.drawing, DrawingGroup):
            # target = self.drawing TODO
            pass
        elif isinstance(self.drawing, GeometryDrawing) and isinstance(self.drawing.geometry, LineGeometry):
            target = self.drawing.geometry
        if target is None:
            return
        algs = [e.name for e in LineClipAlgorithm]
        item, okPressed = QInputDialog.getItem(
            self, "Select Algorithm", "Algorithm:", algs, 0, False)
        if not okPressed or not item:
            return
        rectClipInter = RectClipInteractivity(
            target, self._document.size)
        rectClipInter.clip = None
        rectClipInter.clipAlgorithm = getattr(LineClipAlgorithm, item)
        self._beginInteractive(rectClipInter)

    def _getTransformInteractiveTarget(self) -> Optional[Union[DrawingGroup, Geometry]]:
        if self.drawing is None:
            return
        target = None
        if isinstance(self.drawing, DrawingGroup):
            target = self.drawing
        elif isinstance(self.drawing, GeometryDrawing):
            target = self.drawing.geometry
        if target is None:
            return None
        return target

    def actTransformCreate_triggered(self):
        target = self._getTransformInteractiveTarget()
        if target is None:
            return

        sender = self.sender()
        tname = sender.objectName()[len("actTransform"):]
        assert tname in _TransformInteractiveCreateMap
        transType, interType = _TransformInteractiveCreateMap[tname]

        if not isinstance(target.transform, (type(None), TransformGroup)):
            self.actTransformGroup.trigger()

        tr = transType.__call__()
        self._beginInteractive(interType.__call__(target, tr))

    def actTransformGroup_triggered(self):
        target = self._getTransformInteractiveTarget()
        if target is None:
            return
        if target.transform is None:
            target.transform = TransformGroup()
        elif not isinstance(target.transform, TransformGroup):
            gr = TransformGroup()
            gr.children.append(target.transform)
            target.transform = gr
        else:
            return
        self.documentCommitted.emit(self._document, f"Create TransformGroup")
        self.fresh()

    def actTransformMatrix_triggered(self):
        target = self._getTransformInteractiveTarget()
        if target is None:
            return
        if not isinstance(target.transform, (type(None), TransformGroup)):
            self.actTransformGroup.trigger()
        trans = MatrixTransform()
        default = "\n".join([", ".join(map(str, c))
                             for c in trans.matrix.tolist()])
        text, okPressed = QInputDialog.getMultiLineText(
            self, "Input Matrix", "Matrix:", default)
        if not okPressed or not text:
            return
        lines = str(text).strip().splitlines()
        try:
            for i in range(3):
                t = lines[i].split(",")
                for j in range(3):
                    trans.matrix[i][j] = float(t[j])
        except Exception:
            self.messaged.emit("Matrix is invalid.")
            return
        if isinstance(target.transform, TransformGroup):
            target.transform.children.append(trans)
        else:
            target.transform = trans
        self.documentCommitted.emit(self._document, f"Create MatrixTransform")
        self.fresh()
