import os
from enum import Enum, unique
from typing import Optional

import qtawesome as qta
from PIL import Image
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QMainWindow

import ImagingS.Gui.ui as ui
from ImagingS import Color
from ImagingS.brush import Brush, Brushes, SolidBrush
from ImagingS.document import Document, DocumentFormat
from ImagingS.drawing import NumpyArrayDrawingContext
from ImagingS.Gui import icons
from ImagingS.Gui.app import Application
from ImagingS.Gui.models import (BrushModel, DrawingModel, PropertyModel,
                                 TransformModel)

from . import DocumentEditor, DocumentEditorState


@unique
class MainWindowState(Enum):
    Disable = 0,
    Visual = 1,
    Code = 2


def _create_new_document() -> Document:
    result = Document()
    for name, item in Brushes.__dict__.items():
        if name.startswith("__") and name.endswith("__"):
            continue
        if isinstance(item, Brush):
            result.brushes.append(item)
    return result


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupDockWidget()
        self.setupEditor()
        self.setupIcon()
        self.current_file = None

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actQuit.triggered.connect(self.close)
        self.actNew.triggered.connect(self.actNew_triggered)
        self.actSave.triggered.connect(self.actSave_triggered)
        self.actSaveAs.triggered.connect(self.actSaveAs_triggered)
        self.actOpen.triggered.connect(self.actOpen_triggered)
        self.actExport.triggered.connect(self.actExport_triggered)

        self.actBrushSolid.triggered.connect(self.actBrushSolid_triggered)

        self.actViewVisual.triggered.connect(self.actViewVisual_triggered)
        self.actViewCode.triggered.connect(self.actViewCode_triggered)

        self.modelBrush = BrushModel(self)
        self.trvBrushes.setModel(self.modelBrush)
        self.trvBrushes.clicked.connect(
            self.trvBrushes_clicked)
        self.actBrushRemove.triggered.connect(self.actBrushRemove_triggered)
        self.actBrushClear.triggered.connect(self.actBrushClear_triggered)

        self.modelDrawing = DrawingModel(self)
        self.trvDrawings.setModel(self.modelDrawing)
        self.trvDrawings.clicked.connect(
            self.trvDrawings_clicked)
        self.actDrawingRemove.triggered.connect(
            self.actDrawingRemove_triggered)
        self.actDrawingClear.triggered.connect(self.actDrawingClear_triggered)

        self.modelTransform = TransformModel(self)
        self.trvTransforms.setModel(self.modelTransform)
        self.trvTransforms.clicked.connect(
            self.trvTransforms_clicked)

        self.modelProperties = PropertyModel(self)
        self.trvProperties.setModel(self.modelProperties)

        Application.current().documentChanged.connect(self.app_documentChanged)

        self.actViewVisual.trigger()
        self.actNew.trigger()

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

    def setupEditor(self) -> None:
        self.editor = DocumentEditor()
        self.editor.setObjectName("editor")
        self.gridLayout.addWidget(self.editor, 0, 0, 1, 1)
        self.editor.messaged.connect(self.editor_messaged)

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
        self.actViewCode.setIcon(icons.code)
        self.actViewVisual.setIcon(icons.visual)
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
        doc = Application.current().document
        hasDoc = doc is not None
        self.dwgDrawings.setEnabled(hasDoc)
        if hasDoc:
            self.modelDrawing.fresh(doc.drawings)
            self.trvDrawings.expandAll()
        else:
            self.modelDrawing.fresh()

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
        self.fresh_brushes()
        self.fresh_drawings()
        self.modelProperties.fresh()

        if self.editor.state is not DocumentEditorState.Disable:
            self.editor.disable()

        if doc is not None:
            self.editor.enable(doc)

    def trvBrushes_clicked(self, index):
        item = self.modelBrush.getData(index)
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.modelProperties.fresh()
            self.trvProperties.expandAll()
            self.trvBrushes.clearSelection()

    def trvDrawings_clicked(self, index):
        item = self.modelDrawing.getData(index)
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.modelProperties.fresh()
            self.trvProperties.expandAll()
            self.trvDrawings.clearSelection()

    def trvTransforms_clicked(self, index):
        item = self.modelTransform.getData(index)
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.modelProperties.fresh()
            self.trvProperties.expandAll()
            self.trvTransforms.clearSelection()

    def actViewVisual_triggered(self):
        self.editor.switchVisual()

    def actViewCode_triggered(self):
        self.editor.switchCode()

    def actDrawingRemove_triggered(self):
        indexs = self.trvDrawings.selectedIndexes()
        if len(indexs) == 0:
            return
        r = indexs[0].row()
        del Application.current().document.drawings.children[r]
        self.fresh_drawings()

    def actDrawingClear_triggered(self):
        Application.current().document.drawings.children.clear()
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
                Application.current().document.save(f, DocumentFormat.RAW)
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
                Application.current().document.save(f, DocumentFormat.RAW)
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
                    doc = Document.load(f, DocumentFormat.RAW)
            else:
                with open(fileName, mode="rb") as f:
                    doc = Document.load(f)
            Application.current().document = doc
            self.current_file = fileName

    def actExport_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Export To", "",
            "PNG Image (*.png);; JPEG Image (*.jpeg);; BMP Image (*.bmp)",
            options=options)
        if fileName:
            ext = os.path.splitext(fileName)[1].lstrip(".")
            doc = Application.current().document
            assert doc is not None
            context = NumpyArrayDrawingContext(
                NumpyArrayDrawingContext.create_array(doc.size))

            doc.drawings.render(context)

            Image.fromarray(context.array).save(fileName, ext, quality=95)

    def editor_messaged(self, message: str) -> None:
        self.stbMain.showMessage(message)
