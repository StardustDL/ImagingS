import uuid
from enum import Enum, unique
from typing import Optional, cast

from PyQt5.QtCore import QPointF, QSizeF, pyqtSignal
from PyQt5.QtWidgets import QWidget

import ImagingS.Gui.ui as ui
from ImagingS.brush import Brush
from ImagingS.document import Document
from ImagingS.drawing import Drawing, GeometryDrawing, Pen
from ImagingS.Gui import converters, icons
from ImagingS.Gui.graphic import Canvas
from ImagingS.Gui.interactivity import Interactivity, InteractivityState
from ImagingS.Gui.interactivity.geometry import (GeometryInteractive,
                                                 LineInteractive)


@unique
class VisualPageState(Enum):
    Disable = 0
    Normal = 1
    Interactive = 2


class VisualPage(QWidget, ui.VisualPage):
    messaged = pyqtSignal(str)
    documentChanged = pyqtSignal(Document)
    stateChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupIcon()
        self.setupCanvas()

        # self.actionDrawings = [
        #     self.actDrawingLine,
        #     self.actDrawingPolygon,
        #     self.actDrawingCurve,
        #     self.actDrawingEllipse,
        # ]

        # self.actionTransforms = [
        #     self.actTransformTranslate,
        #     self.actTransformScale,
        #     self.actTransformRotate,
        #     self.actTransformSkew,
        #     self.actTransformMatrix,
        #     self.actTransformGroup,
        # ]

        self.actDrawingLine.triggered.connect(self.actDrawingLine_triggered)

        self.setEnabled(False)
        self._drawing = None
        self._state = VisualPageState.Disable

    def setupIcon(self):
        self.actDrawingLine.setIcon(icons.lineGeometry)
        self.actDrawingCurve.setIcon(icons.curveGeometry)
        self.actDrawingEllipse.setIcon(icons.ellipseGeometry)
        self.actDrawingPolygon.setIcon(icons.polygonGeometry)
        self.actTransformSkew.setIcon(icons.skewTransform)
        self.actTransformScale.setIcon(icons.scaleTransform)
        self.actTransformTranslate.setIcon(icons.translateTransform)
        self.actTransformRotate.setIcon(icons.rotateTransform)
        self.actTransformMatrix.setIcon(icons.matrixTransform)
        self.actTransformGroup.setIcon(icons.transformGroup)

    def setupCanvas(self):
        self.cvsMain = Canvas(self.widMain)
        self.cvsMain.setObjectName("cvsMain")
        self.grdMain.addWidget(self.cvsMain, 0, 0, 1, 1)
        self.cvsMain.resize(QSizeF(600, 600))
        self.cvsMain.mousePositionMoved.connect(
            self.cvsMain_mousePositionMoved)

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

    def cvsMain_mousePositionMoved(self, point: QPointF):
        self.messaged.emit(str((round(point.x()), round(point.y()))))

    def _emptyGeometryDrawing(self) -> GeometryDrawing:
        drawing = GeometryDrawing()
        drawing.id = str(uuid.uuid1())
        if self.brush is not None:
            drawing.stroke = Pen.create(self.brush)
        return drawing

    def actDrawingLine_triggered(self):
        inter = LineInteractive(
            self._emptyGeometryDrawing(), self._document.size)
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
            if isinstance(inter, GeometryInteractive):
                drawing = cast(GeometryInteractive, inter).target
                self._document.drawings.children.append(drawing)
                self.documentChanged.emit(self._document)
        self.fresh()
