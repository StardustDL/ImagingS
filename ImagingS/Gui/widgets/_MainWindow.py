from ImagingS.core.drawing import Drawing
from typing import Optional
from ImagingS.Gui import icons
import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color
from ImagingS.core.brush import Brushes, SolidBrush, Brush
from ImagingS.Gui.models import BrushModel, PropertyModel, DrawingModel
import qtawesome as qta

from . import CodePage, VisualPage

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog

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
        self.setupVisual()
        self.setupCode()
        self.setupDockWidget()
        self.setupIcon()
        self.current_file = None

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actQuit.triggered.connect(self.close)
        self.actNew.triggered.connect(self.actNew_triggered)
        self.actSave.triggered.connect(self.actSave_triggered)
        self.actSaveAs.triggered.connect(self.actSaveAs_triggered)
        self.actOpen.triggered.connect(self.actOpen_triggered)

        self.actBrushSolid.triggered.connect(self.actBrushSolid_triggered)
        self.actBrushRemove.triggered.connect(self.actBrushRemove_triggered)
        self.actBrushClear.triggered.connect(self.actBrushClear_triggered)

        self.actDrawingRemove.triggered.connect(
            self.actDrawingRemove_triggered)
        self.actDrawingClear.triggered.connect(self.actDrawingClear_triggered)

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

        self.widCode.uploaded.connect(self.widCode_uploaded)

        self.tbxMain.setCurrentIndex(0)  # Visual

        self.tbxMain.currentChanged.connect(self.tbxMain_currentChanged)

        Application.current().documentChanged.connect(self.app_documentChanged)
        self.actNew.trigger()

    def setupCode(self):
        self.widCode = CodePage()
        self.widCode.setObjectName("widCode")
        self.grdCode.addWidget(self.widCode, 0, 0, 1, 1)
        self.widCode.messaged.connect(self.widVisualCode_messaged)

    def setupVisual(self):
        self.widVisual = VisualPage()
        self.widVisual.setObjectName("widVisual")
        self.grdVisual.addWidget(self.widVisual, 0, 0, 1, 1)
        self.widVisual.messaged.connect(self.widVisualCode_messaged)
        self.widVisual.drawingCreated.connect(self.widVisual_drawingCreated)

        for act in self.widVisual.actionDrawings:
            self.mnuDrawing.addAction(act)

        for act in self.widVisual.actionTransforms:
            self.mnuTransform.addAction(act)

    def setupDockWidget(self):
        self.actToggleBrushes = self.dwgBrushes.toggleViewAction()
        self.actToggleBrushes.setShortcut("Ctrl+Shift+B")
        self.actToggleProperties = self.dwgProperties.toggleViewAction()
        self.actToggleProperties.setShortcut("Ctrl+Shift+P")
        self.actToggleDrawings = self.dwgDrawings.toggleViewAction()
        self.actToggleDrawings.setShortcut("Ctrl+Shift+D")
        self.actToggleTransforms = self.dwgTransforms.toggleViewAction()
        self.actToggleTransforms.setShortcut("Ctrl+Shift+T")

        self.tabifyDockWidget(self.dwgDrawings, self.dwgBrushes)
        self.tabifyDockWidget(self.dwgBrushes, self.dwgTransforms)
        self.dwgDrawings.raise_()

        viewActions = [self.actToggleDrawings, self.actToggleBrushes,
                       self.actToggleTransforms, self.actToggleProperties]
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
        self.actBrushSolid.setIcon(icons.solidBrush)
        self.actBrushRemove.setIcon(qta.icon("mdi.close", color="red"))
        self.actDrawingRemove.setIcon(qta.icon("mdi.close", color="red"))
        self.actTransformRemove.setIcon(qta.icon("mdi.close", color="red"))
        self.actBrushClear.setIcon(qta.icon("mdi.delete", color="red"))
        self.actDrawingClear.setIcon(qta.icon("mdi.delete", color="red"))
        self.actTransformClear.setIcon(qta.icon("mdi.delete", color="red"))
        self.dwgBrushes.setWindowIcon(icons.brush)
        self.dwgDrawings.setWindowIcon(icons.drawing)
        self.dwgProperties.setWindowIcon(icons.property)
        self.dwgTransforms.setWindowIcon(icons.transform)
        self.actToggleDrawings.setIcon(icons.drawing)
        self.actToggleBrushes.setIcon(icons.brush)
        self.actToggleProperties.setIcon(icons.property)
        self.actToggleTransforms.setIcon(icons.transform)
        self.tbxMain.setItemIcon(0, qta.icon("mdi.image"))
        self.tbxMain.setItemIcon(1, qta.icon("mdi.code-tags"))
        self.setWindowIcon(qta.icon("mdi.pencil-box-multiple", color="purple"))

    @property
    def current_file(self) -> Optional[str]:
        return self._current_file

    @current_file.setter
    def current_file(self, value: Optional[str]) -> None:
        self._current_file = os.path.realpath(value) if value else None
        if self._current_file is None:
            if Application.current().document is None:
                self.setWindowTitle("ImagingS")
            else:
                self.setWindowTitle("Untitled - ImagingS")
        else:
            filename = os.path.split(self._current_file)[1].rstrip(".isd.json")
            self.setWindowTitle(f"{filename} - ImagingS")

    def fresh_brushes(self):
        self.modelBrush.clear_items()

        doc = Application.current().document
        hasDoc = doc is not None

        if hasDoc:
            for br in doc.brushes:
                self.modelBrush.append(br)

        self.dwgBrushes.setEnabled(hasDoc)

    def fresh_drawings(self):
        self.modelDrawing.clear_items()
        doc = Application.current().document
        hasDoc = doc is not None
        if hasDoc:
            for br in doc.drawings:
                self.modelDrawing.append(br)
        self.widVisual.document = doc
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
        self.tbxMain.setEnabled(hasDoc)
        self.fresh_brushes()
        self.fresh_drawings()

        self.widCode.document = doc
        self.widVisual.document = doc

        self.modelProperties.fresh(doc)
        self.trvProperties.expandAll()

    def widVisualCode_messaged(self, message: str) -> None:
        self.stbMain.showMessage(message)

    def widVisual_drawingCreated(self, drawing: Drawing) -> None:
        self.modelDrawing.append(drawing)

    def widCode_uploaded(self):
        tdoc = self.widCode.load_document()
        if tdoc is None:
            self.stbMain.showMessage("Load document from code failed.")
        else:
            Application.current().document = tdoc

    def tbxMain_currentChanged(self, index):
        if index == 0:  # Visual
            self.widCode.upload()
        else:  # Code
            self.widCode.fresh()

    def trvBrushes_clicked(self, index):
        r = index.row()
        doc = Application.current().document
        item = doc.brushes[r]
        if self.modelProperties.obj is not item:
            self.widVisual.brush = item
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.widVisual.brush = None
            self.modelProperties.fresh(doc)
            self.trvProperties.expandAll()
            self.trvBrushes.clearSelection()

    def trvDrawings_clicked(self, index):
        r = index.row()
        doc = Application.current().document
        item = doc.drawings.at(r)
        if self.modelProperties.obj is not item:
            self.widVisual.drawing = item
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.widVisual.drawing = None
            self.modelProperties.fresh(doc)
            self.trvProperties.expandAll()
            self.trvDrawings.clearSelection()

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

    def actClose_triggered(self):
        Application.current().document = None
        self.current_file = None

    def actNew_triggered(self):
        Application.current().document = _create_new_document()

    def actSave_triggered(self):
        file = self.current_file
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
        self.current_file = fileName

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
            self.current_file = fileName
