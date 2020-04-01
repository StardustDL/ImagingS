from typing import Optional
import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color, brush
from ImagingS.core.brush import Brushes, Brush
from ImagingS.Gui.models import BrushModel, PropertyModel
import qtawesome as qta

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog

import os


def _create_new_document() -> Document:
    result = Document()
    for name in dir(Brushes):
        item = getattr(Brushes, name)
        if isinstance(item, Brush):
            result.brushes.append(item)
    return result


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupDockWidget()
        self.setupIcon()
        self._current_file: Optional[str] = None

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actQuit.triggered.connect(self.close)
        self.actNew.triggered.connect(self.actNew_triggered)
        self.actSave.triggered.connect(self.actSave_triggered)
        self.actSaveAs.triggered.connect(self.actSaveAs_triggered)
        self.actOpen.triggered.connect(self.actOpen_triggered)
        self.actBrushSolid.triggered.connect(self.actBrushSolid_triggered)

        self.modelBrush = BrushModel(self)
        self.trvBrushes.setModel(self.modelBrush)
        self.trvBrushes.clicked.connect(
            self.trvBrushes_clicked)

        self.modelProperties = PropertyModel(self)
        self.trvProperties.setModel(self.modelProperties)

        self.tabifyDockWidget(self.dwgBrushes, self.dwgTransforms)
        self.dwgBrushes.raise_()

        Application.current().documentChanged.connect(self.app_documentChanged)
        self.actNew.trigger()

    def setupDockWidget(self):
        self.actToggleBrushes = self.dwgBrushes.toggleViewAction()
        self.actToggleProperties = self.dwgProperties.toggleViewAction()
        self.actToggleDrawings = self.dwgDrawings.toggleViewAction()
        self.actToggleTransforms = self.dwgTransforms.toggleViewAction()

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
        self.actToggleDrawings.setIcon(qta.icon("mdi.drawing"))
        self.actToggleBrushes.setIcon(qta.icon("mdi.brush"))
        self.actToggleTransforms.setIcon(qta.icon("mdi.axis"))
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
        self.actBrushSolid.setIcon(qta.icon("mdi.solid"))
        self.actBrushRemove.setIcon(qta.icon("mdi.delete", color="red"))
        self.actDrawingRemove.setIcon(qta.icon("mdi.delete", color="red"))
        self.actBrushClear.setIcon(qta.icon("mdi.delete-sweep", color="red"))
        self.actDrawingClear.setIcon(qta.icon("mdi.delete-sweep", color="red"))
        self.dwgBrushes.setWindowIcon(qta.icon("mdi.brush"))
        self.dwgDrawings.setWindowIcon(qta.icon("mdi.drawing"))
        self.dwgTransforms.setWindowIcon(qta.icon("mdi.axis"))
        self.dwgProperties.setWindowIcon(qta.icon("mdi.database"))
        self.tlbWindow.setWindowIcon(qta.icon("mdi.toolbox"))
        self.setWindowIcon(qta.icon("mdi.pencil-box-multiple", color="purple"))

    @property
    def current_file(self) -> Optional[str]:
        return self._current_file

    @current_file.setter
    def current_file(self, value: Optional[str]) -> None:
        self._current_file = value
        if self._current_file is None:
            if Application.current().document is None:
                self.setWindowTitle("ImagingS")
            else:
                self.setWindowTitle(f"Untitled - ImagingS")
        else:
            filename = os.path.split(self._current_file)[
                1].rstrip(".isd.json")
            self.setWindowTitle(f"{filename} - ImagingS")

    def app_documentChanged(self):
        doc = Application.current().document
        hasDoc = doc is not None
        self.actClose.setEnabled(hasDoc)
        self.actSave.setEnabled(hasDoc)
        self.actExport.setEnabled(hasDoc)
        self.gvwMain.setEnabled(hasDoc)
        self.mnuDrawing.setEnabled(hasDoc)
        self.mnuTransform.setEnabled(hasDoc)
        self.mnuBrush.setEnabled(hasDoc)
        self.dwgDrawings.setEnabled(hasDoc)
        self.dwgBrushes.setEnabled(hasDoc)
        self.dwgProperties.setEnabled(hasDoc)
        self.dwgTransforms.setEnabled(hasDoc)
        self.tlbWindow.setEnabled(hasDoc)

        if hasDoc:
            self.modelBrush.clear_items()
            for br in doc.brushes:
                self.modelBrush.append(br)
            self.modelProperties.fresh(None)
        else:
            self.modelBrush.clear_items()
            self.modelProperties.fresh(None)

        self.current_file = self.current_file  # update title

    def trvBrushes_clicked(self, index):
        r = index.row()
        item = Application.current().document.brushes[r]
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)

    def actBrushSolid_triggered(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        br = brush.SolidBrush(Color(color.red(), color.green(), color.blue()))
        Application.current().document.brushes.append(br)
        self.modelBrush.append(br)

    def actClose_triggered(self):
        self.current_file = None
        Application.current().document = None

    def actNew_triggered(self):
        Application.current().document = _create_new_document()

    def actSave_triggered(self):
        if self.current_file is None:
            self.actSaveAs_triggered()
            return

        with open(self.current_file, mode="w+") as f:
            Application.current().document.save(f)

    def actSaveAs_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save as", "", "ImagingS document (*.isd.json)", options=options)
        if not fileName:
            return

        self.current_file = fileName
        with open(fileName, mode="w+") as f:
            Application.current().document.save(f)
        self.app_documentChanged()

    def actOpen_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "ImagingS document (*.isd.json)", options=options)
        if fileName:
            self.current_file = fileName
            with open(fileName, mode="r") as f:
                Application.current().document = Document.load(f)
