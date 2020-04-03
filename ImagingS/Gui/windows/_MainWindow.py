from ImagingS.core.drawing import Drawing
from typing import Optional
import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color
from ImagingS.core.brush import Brushes, SolidBrush, Brush
from ImagingS.core.geometry import Line, Curve, Polygon, Ellipse, Geometry
from ImagingS.Gui.models import BrushModel, PropertyModel, DrawingModel
from ImagingS.Gui.graphics import Canvas, converters
from ImagingS.Gui.interactive import LineInteractive, PolygonInteractive, CurveInteractive, EllipseInteractive, Interactive
from ImagingS.Gui.interactive import TranslateTransformInteractive, SkewTransformInteractive, RotateTransformInteractive
import uuid
import qtawesome as qta

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog
from PyQt5.QtCore import QSizeF

import os


def _create_new_document() -> Document:
    result = Document()
    for name, item in Brushes.__dict__.items():
        if name.startswith("__") and name.endswith("__"):
            continue
        br = item.__func__()  # static method . __func__
        if isinstance(br, Brush):
            result.brushes.append(br)
    return result


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupCanvas()
        self.setupDockWidget()
        self.setupIcon()
        self.set_current_file(None)

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actQuit.triggered.connect(self.close)
        self.actNew.triggered.connect(self.actNew_triggered)
        self.actSave.triggered.connect(self.actSave_triggered)
        self.actSaveAs.triggered.connect(self.actSaveAs_triggered)
        self.actOpen.triggered.connect(self.actOpen_triggered)

        self.actBrushSolid.triggered.connect(self.actBrushSolid_triggered)
        self.actBrushRemove.triggered.connect(self.actBrushRemove_triggered)
        self.actBrushClear.triggered.connect(self.actBrushClear_triggered)

        self.actDrawingCurve.triggered.connect(self.actDrawingCurve_triggered)
        self.actDrawingLine.triggered.connect(self.actDrawingLine_triggered)
        self.actDrawingEllipse.triggered.connect(
            self.actDrawingEllipse_triggered)
        self.actDrawingPolygon.triggered.connect(
            self.actDrawingPolygon_triggered)
        self.actDrawingRemove.triggered.connect(
            self.actDrawingRemove_triggered)
        self.actDrawingClear.triggered.connect(self.actDrawingClear_triggered)

        self.actTransformTranslate.triggered.connect(
            self.actTransformTranslate_triggered)
        self.actTransformSkew.triggered.connect(
            self.actTransformSkew_triggered)
        self.actTransformRotate.triggered.connect(
            self.actTransformRotate_triggered)

        self.modelBrush = BrushModel(self)
        self.trvBrushes.setModel(self.modelBrush)
        self.trvBrushes.clicked.connect(
            self.trvBrushes_clicked)

        self.modelDrawing = DrawingModel(self)
        self.trvDrawings.setModel(self.modelDrawing)
        self.trvDrawings.clicked.connect(
            self.trvDrawings_clicked)

        self.modelProperties = PropertyModel(self)
        self.trvProperties.setModel(self.modelProperties)

        Application.current().documentChanged.connect(self.app_documentChanged)
        self.actNew.trigger()

    def setupCanvas(self):
        self._interactive: Optional[Interactive] = None

        self.gvwMain = Canvas(self.centralwidget)
        self.gvwMain.setEnabled(True)
        self.gvwMain.setObjectName("gvwMain")
        self.gridLayout.addWidget(self.gvwMain, 0, 0, 1, 1)
        self.gvwMain.resize(QSizeF(600, 600))

    def setupDockWidget(self):
        self.actToggleBrushes = self.dwgBrushes.toggleViewAction()
        self.actToggleBrushes.setShortcut("Ctrl+Shift+B")
        self.actToggleProperties = self.dwgProperties.toggleViewAction()
        self.actToggleProperties.setShortcut("Ctrl+Shift+P")
        self.actToggleDrawings = self.dwgDrawings.toggleViewAction()
        self.actToggleDrawings.setShortcut("Ctrl+Shift+D")

        self.tabifyDockWidget(self.dwgBrushes, self.dwgProperties)
        self.dwgBrushes.raise_()

        viewActions = [self.actToggleDrawings, self.actToggleBrushes,
                       self.actToggleProperties]
        self.mnuView.addActions(viewActions)

    def setupIcon(self):
        self.actNew.setIcon(qta.icon("mdi.file"))
        self.actOpen.setIcon(qta.icon("mdi.folder-open"))
        self.actSave.setIcon(qta.icon("mdi.content-save"))
        self.actSaveAs.setIcon(qta.icon("mdi.content-save-move"))
        self.actExport.setIcon(qta.icon("mdi.export"))
        self.actClose.setIcon(qta.icon("mdi.close"))
        self.actQuit.setIcon(qta.icon("mdi.exit-to-app"))
        self.actUndo.setIcon(qta.icon("mdi.undo"))
        self.actRedo.setIcon(qta.icon("mdi.redo"))
        self.actToggleDrawings.setIcon(qta.icon("mdi.drawing"))
        self.actToggleBrushes.setIcon(qta.icon("mdi.brush"))
        self.actToggleProperties.setIcon(qta.icon("mdi.database"))
        self.actDrawingLine.setIcon(qta.icon("mdi.vector-line"))
        self.actDrawingCurve.setIcon(qta.icon("mdi.vector-curve"))
        self.actDrawingEllipse.setIcon(qta.icon("mdi.vector-ellipse"))
        self.actDrawingPolygon.setIcon(qta.icon("mdi.vector-polygon"))
        self.actTransformSkew.setIcon(qta.icon("mdi.skew-more"))
        self.actTransformScale.setIcon(qta.icon("mdi.relative-scale"))
        self.actTransformTranslate.setIcon(qta.icon("mdi.cursor-move"))
        self.actTransformRotate.setIcon(qta.icon("mdi.rotate-left"))
        self.actTransformMatrix.setIcon(qta.icon("mdi.matrix"))
        self.actTransformClip.setIcon(qta.icon("mdi.crop"))
        self.actTransformGroup.setIcon(qta.icon("mdi.group"))
        self.actBrushSolid.setIcon(qta.icon("mdi.solid"))
        self.actBrushRemove.setIcon(qta.icon("mdi.delete", color="red"))
        self.actDrawingRemove.setIcon(qta.icon("mdi.delete", color="red"))
        self.actBrushClear.setIcon(qta.icon("mdi.delete-sweep", color="red"))
        self.actDrawingClear.setIcon(qta.icon("mdi.delete-sweep", color="red"))
        self.dwgBrushes.setWindowIcon(qta.icon("mdi.brush"))
        self.dwgDrawings.setWindowIcon(qta.icon("mdi.drawing"))
        self.dwgProperties.setWindowIcon(qta.icon("mdi.database"))
        self.tlbWindow.setWindowIcon(qta.icon("mdi.toolbox"))
        self.setWindowIcon(qta.icon("mdi.pencil-box-multiple", color="purple"))

    def current_file(self) -> Optional[str]:
        return self._current_file

    def set_current_file(self, value: Optional[str]) -> None:
        self._current_file = os.path.realpath(value) if value else None
        if self._current_file is None:
            if Application.current().document is None:
                self.setWindowTitle("ImagingS")
            else:
                self.setWindowTitle("Untitled - ImagingS")
        else:
            filename = os.path.split(self._current_file)[1].rstrip(".isd.json")
            self.setWindowTitle(f"{filename} - ImagingS")

    def current_drawing(self) -> Optional[Drawing]:
        return self._current_drawing

    def set_current_drawing(self, value: Optional[Drawing]) -> None:
        self._current_drawing = value
        if value is not None:
            self.gvwMain.select(value.id)
            self.stbMain.showMessage(f"Current drawing: {value.id}")
        else:
            self.gvwMain.select(None)
            self.stbMain.showMessage("")

    def current_brush(self) -> Optional[Brush]:
        return self._current_brush

    def set_current_brush(self, value: Optional[Brush]) -> None:
        self._current_brush = value
        if value is not None:
            if isinstance(value, SolidBrush):
                self.stbMain.showMessage(
                    f"Current brush: {value.color.to_hex()}")
        else:
            self.stbMain.showMessage("")

    def fresh_brushes(self):
        self.modelBrush.clear_items()

        doc = Application.current().document
        hasDoc = doc is not None

        if hasDoc:
            for br in doc.brushes:
                self.modelBrush.append(br)

        self.set_current_brush(None)
        self.dwgBrushes.setEnabled(hasDoc)

    def fresh_drawings(self):
        self.modelDrawing.clear_items()
        self.gvwMain.clear()

        doc = Application.current().document
        hasDoc = doc is not None

        if hasDoc:
            self.gvwMain.resize(converters.convert_size(doc.size))
            for br in doc.drawings:
                self.modelDrawing.append(br)
                self.gvwMain.add(br)

        self.set_current_drawing(None)

        self.gvwMain.setEnabled(hasDoc)
        self.dwgDrawings.setEnabled(hasDoc)

    def app_documentChanged(self):
        doc = Application.current().document
        hasDoc = doc is not None
        self.actClose.setEnabled(hasDoc)
        self.actSave.setEnabled(hasDoc)
        self.actSaveAs.setEnabled(hasDoc)
        self.actExport.setEnabled(hasDoc)
        self.mnuDrawing.setEnabled(hasDoc)
        self.mnuTransform.setEnabled(hasDoc)
        self.mnuBrush.setEnabled(hasDoc)
        self.dwgProperties.setEnabled(hasDoc)
        self.tlbWindow.setEnabled(hasDoc)
        self.fresh_brushes()
        self.fresh_drawings()
        self.modelProperties.fresh(doc)
        self.trvProperties.expandAll()

    def trvBrushes_clicked(self, index):
        r = index.row()
        doc = Application.current().document
        item = doc.brushes[r]
        if self.modelProperties.obj is not item:
            self.set_current_brush(item)
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.set_current_brush(None)
            self.modelProperties.fresh(doc)
            self.trvProperties.expandAll()
            self.trvBrushes.clearSelection()

    def trvDrawings_clicked(self, index):
        r = index.row()
        doc = Application.current().document
        item = doc.drawings.at(r)
        if self.modelProperties.obj is not item:
            self.set_current_drawing(item)
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.set_current_drawing(None)
            self.modelProperties.fresh(doc)
            self.trvProperties.expandAll()
            self.trvDrawings.clearSelection()

    def resetDrawingActionChecked(self, checkedAction=None):
        for act in self.mnuDrawing.actions():
            if act.isCheckable() and act is not checkedAction:
                act.setChecked(False)

    def _create_geometry(self, geo: Geometry) -> None:
        brush = self.current_brush()
        if brush is not None:
            geo.stroke = brush
        self.gvwMain.add(geo)

    def _set_interactive(self, inter: Optional[Interactive]) -> None:
        self._interactive = inter
        if self._interactive is not None:
            self.gvwMain.interactive = self._interactive

    def interDrawing_ended(self) -> None:
        if self._interactive is None:
            return
        inter = self._interactive
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
            Application.current().document.drawings.append(drawing)
            self.modelDrawing.append(drawing)
            self.set_current_drawing(drawing)
        else:
            self.gvwMain.remove(inter.drawing.id)
        self._set_interactive(None)

    def interTransform_ended(self) -> None:
        if self._interactive is None:
            return
        inter = self._interactive
        drawing = self.current_drawing()
        if drawing is None:
            return
        drawing.refresh_boundingArea()
        if inter.state == Interactive.S_Success:
            pass
        else:
            drawing.transform = None
        self._set_interactive(None)

    def actDrawingCurve_triggered(self):
        if not self.actDrawingCurve.isChecked():
            self._set_interactive(None)
            return
        self.resetDrawingActionChecked(self.actDrawingCurve)
        curve = Curve()
        curve.id = str(uuid.uuid1())
        self._create_geometry(curve)
        inter = CurveInteractive(curve)
        inter.ended.connect(self.interDrawing_ended)
        self._set_interactive(inter)

    def actDrawingPolygon_triggered(self):
        if not self.actDrawingPolygon.isChecked():
            self._set_interactive(None)
            return
        self.resetDrawingActionChecked(self.actDrawingPolygon)
        polygon = Polygon()
        polygon.id = str(uuid.uuid1())
        self._create_geometry(polygon)
        inter = PolygonInteractive(polygon)
        inter.ended.connect(self.interDrawing_ended)
        self._set_interactive(inter)

    def actDrawingEllipse_triggered(self):
        if not self.actDrawingEllipse.isChecked():
            self._set_interactive(None)
            return
        self.resetDrawingActionChecked(self.actDrawingEllipse)
        ell = Ellipse()
        ell.id = str(uuid.uuid1())
        self._create_geometry(ell)
        inter = EllipseInteractive(ell)
        inter.ended.connect(self.interDrawing_ended)
        self._set_interactive(inter)

    def actDrawingLine_triggered(self):
        if not self.actDrawingLine.isChecked():
            self._set_interactive(None)
            return
        self.resetDrawingActionChecked(self.actDrawingLine)
        line = Line()
        line.id = str(uuid.uuid1())
        self._create_geometry(line)
        inter = LineInteractive(line)
        inter.ended.connect(self.interDrawing_ended)
        self._set_interactive(inter)

    def actDrawingRemove_triggered(self):
        indexs = self.trvDrawings.selectedIndexes()
        if len(indexs) == 0:
            return
        r = indexs[0].row()
        dr = Application.current().document.drawings.at(r)
        del Application.current().document.drawings[dr.id]
        self.fresh_drawings()

    def actDrawingClear_triggered(self):
        Application.current().document.drawings.clear()
        self.fresh_drawings()

    def actBrushSolid_triggered(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        br = SolidBrush.create(Color.create(
            color.red(), color.green(), color.blue()))
        Application.current().document.brushes.append(br)
        self.modelBrush.append(br)

    def actBrushRemove_triggered(self):
        indexs = self.trvBrushes.selectedIndexes()
        if len(indexs) == 0:
            return
        r = indexs[0].row()
        Application.current().document.brushes.remove(
            Application.current().document.brushes[r])
        self.fresh_brushes()

    def actBrushClear_triggered(self):
        Application.current().document.brushes.clear()
        self.fresh_brushes()

    def actTransformTranslate_triggered(self):
        drawing = self.current_drawing()
        if drawing is None:
            return
        inter = TranslateTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self._set_interactive(inter)

    def actTransformSkew_triggered(self):
        drawing = self.current_drawing()
        if drawing is None:
            return
        inter = SkewTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self._set_interactive(inter)

    def actTransformRotate_triggered(self):
        drawing = self.current_drawing()
        if drawing is None:
            return
        inter = RotateTransformInteractive(drawing)
        inter.ended.connect(self.interTransform_ended)
        self._set_interactive(inter)

    def actClose_triggered(self):
        Application.current().document = None
        self.set_current_file(None)

    def actNew_triggered(self):
        Application.current().document = _create_new_document()

    def actSave_triggered(self):
        file = self.current_file()
        if file is None:
            self.actSaveAs_triggered()
            return
        if file.endswith(".isd.json"):
            with open(file, mode="w+") as f:
                Application.current().document.save(f, Document.FILE_RAW)
        else:
            with open(file, mode="wb") as f:
                Application.current().document.save(f)

    def actSaveAs_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if not fileName:
            return

        if fileName.endswith(".isd.json"):
            with open(fileName, mode="w+") as f:
                Application.current().document.save(f, Document.FILE_RAW)
        else:
            with open(fileName, mode="wb") as f:
                Application.current().document.save(f)
        self.set_current_file(fileName)

    def actOpen_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if fileName:
            if fileName.endswith(".isd.json"):
                with open(fileName, mode="r") as f:
                    doc = Document.load(f, Document.FILE_RAW)
            else:
                with open(fileName, mode="rb") as f:
                    doc = Document.load(f)
            Application.current().document = doc
            self.set_current_file(fileName)
