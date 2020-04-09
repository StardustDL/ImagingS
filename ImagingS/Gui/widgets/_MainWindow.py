import os
from enum import Enum, unique
from typing import Optional

import qtawesome as qta
from PIL import Image
from PyQt5.QtWidgets import QColorDialog, QDialog, QFileDialog, QMainWindow

import ImagingS.Gui.ui as ui
from ImagingS import Color
from ImagingS.brush import SolidBrush
from ImagingS.document import Document, DocumentFormat
from ImagingS.drawing import NumpyArrayDrawingContext
from ImagingS.Gui import icons
from ImagingS.Gui.models import (BrushModel, DrawingModel, PropertyModel,
                                 TransformModel)

from . import (DocumentEditor, DocumentEditorState, NewDocumentDialog,
               VisualPageState)


@unique
class MainWindowState(Enum):
    Disable = 0,
    Visual = 1,
    Code = 2


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupDockWidget()
        self.setupStatusBar()
        self.setupEditor()
        self.setupIcon()
        self._file = None
        self._document = None

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

        self._freshAll()

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

    def setupStatusBar(self) -> None:
        pass

    def setupEditor(self) -> None:
        self.editor = DocumentEditor()
        self.editor.setObjectName("editor")
        self.gridLayout.addWidget(self.editor, 0, 0, 1, 1)
        self.editor.messaged.connect(self.editor_messaged)
        self.editor.documentChanged.connect(self.editor_documentChanged)
        self.editor.stateChanged.connect(self.editor_stateChanged)
        self.editor.visual.stateChanged.connect(
            self.editor_visual_stateChanged)

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
    def file(self) -> Optional[str]:
        return self._file

    @file.setter
    def file(self, value: Optional[str]) -> None:
        self._file = os.path.realpath(value) if value else None
        self._freshTitle()

    @property
    def document(self) -> Optional[Document]:
        return self._document

    @document.setter
    def document(self, value: Optional[Document]) -> None:
        self._document = value
        self._freshTitle()

    def _freshTitle(self) -> None:
        if self.file is None:
            if self.document is None:
                self.setWindowTitle("ImagingS")
            else:
                self.setWindowTitle("Untitled - ImagingS")
        else:
            self.setWindowTitle(f"{self.file} - ImagingS")

    def _freshBrushes(self):
        hasDoc = self.document is not None
        self.dwgBrushes.setEnabled(hasDoc)
        self.modelBrush.clear_items()
        if hasDoc:
            for br in self.document.brushes:
                self.modelBrush.append(br)

    def _freshDrawings(self):
        hasDoc = self.document is not None
        self.dwgDrawings.setEnabled(hasDoc)
        if hasDoc:
            self.modelDrawing.fresh(self.document.drawings)
            self.trvDrawings.expandAll()
        else:
            self.modelDrawing.fresh()

    def _freshProperties(self):
        hasDoc = self.document is not None
        self.modelProperties.fresh()
        self.dwgProperties.setEnabled(hasDoc)

    def _freshDockWidgets(self):
        self._freshProperties()
        self._freshBrushes()
        self._freshDrawings()

    def _freshActions(self):
        hasDoc = self.document is not None

        self.actClose.setEnabled(hasDoc)
        self.actSave.setEnabled(hasDoc)
        self.actSaveAs.setEnabled(hasDoc)
        self.actExport.setEnabled(hasDoc)

        self.mnuEdit.setEnabled(hasDoc)
        self.mnuView.setEnabled(hasDoc)
        self.mnuDrawing.setEnabled(hasDoc)
        self.mnuTransform.setEnabled(hasDoc)
        self.mnuBrush.setEnabled(hasDoc)
        self.mnuTool.setEnabled(hasDoc)

        isVisualNormal = self.editor.state is DocumentEditorState.Visual and self.editor.visual.state is VisualPageState.Normal
        self.actDrawingClear.setEnabled(isVisualNormal)
        self.actBrushClear.setEnabled(isVisualNormal)
        self.actTransformClear.setEnabled(isVisualNormal)
        self.actDrawingRemove.setEnabled(isVisualNormal)
        self.actBrushRemove.setEnabled(isVisualNormal)
        self.actTransformRemove.setEnabled(isVisualNormal)
        self.mnuDrawing.setEnabled(isVisualNormal)
        self.mnuTransform.setEnabled(isVisualNormal)
        self.mnuBrush.setEnabled(isVisualNormal)
        self.mnuTool.setEnabled(isVisualNormal)

    def _freshEditor(self):
        if self.editor.state is not DocumentEditorState.Disable:
            self.editor.disable()

        if self.document is not None:
            self.editor.enable(self.document)

    def _freshAll(self):
        self._freshTitle()
        self._freshDockWidgets()
        self._freshEditor()
        self._freshActions()

    def trvBrushes_clicked(self, index):
        item = self.modelBrush.getData(index)
        if self.modelProperties.obj is not item:
            self.editor.visual.brush = item
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.editor.visual.brush = None
            self.modelProperties.fresh()
            self.trvBrushes.clearSelection()

    def trvDrawings_clicked(self, index):
        item = self.modelDrawing.getData(index)
        if self.modelProperties.obj is not item:
            self.editor.visual.drawing = item
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.editor.visual.drawing = None
            self.modelProperties.fresh()
            self.trvDrawings.clearSelection()

    def trvTransforms_clicked(self, index):
        item = self.modelTransform.getData(index)
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.modelProperties.fresh()
            self.trvTransforms.clearSelection()

    def actViewVisual_triggered(self):
        self.editor.switchVisual()

    def actViewCode_triggered(self):
        self.editor.switchCode()

    def actDrawingRemove_triggered(self):
        indexs = self.trvDrawings.selectedIndexes()
        if len(indexs) == 0:
            return
        item = self.modelDrawing.getData(indexs[0])
        del self.document.drawings.children[item]
        self._freshDrawings()
        self.editor.fresh()
        self.stbMain.showMessage(f"Deleted drawing ({item}).")

    def actDrawingClear_triggered(self):
        self.document.drawings.children.clear()
        self._freshDrawings()
        self.editor.fresh()
        self.stbMain.showMessage("Cleared drawings.")

    def actBrushSolid_triggered(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        br = SolidBrush.create(Color.create(
            color.red(), color.green(), color.blue()))
        self.document.brushes.append(br)
        self._freshBrushes()
        self.stbMain.showMessage(
            f"Add new brush ({br}).")

    def actBrushRemove_triggered(self):
        indexs = self.trvBrushes.selectedIndexes()
        if len(indexs) == 0:
            return
        item = self.modelBrush.getData(indexs[0])
        self.document.brushes.remove(item)
        self._freshBrushes()
        self.stbMain.showMessage(
            f"Deleted brush ({item}).")

    def actBrushClear_triggered(self):
        self.document.brushes.clear()
        self._freshBrushes()
        self.stbMain.showMessage("Cleared brushes.")

    def actClose_triggered(self):
        self.document = None
        self.file = None
        self._freshAll()

    def actNew_triggered(self):
        newDialog = NewDocumentDialog()
        if newDialog.exec_() == QDialog.Accepted:
            doc = Document()
            doc.size = newDialog.documentSize
            self.document = doc
            self._freshAll()
            self.stbMain.showMessage(
                f"Created new document with size ({doc.size.width}, {doc.size.height}).")

    def actSave_triggered(self):
        file = self.file
        if file is None:
            self.actSaveAs_triggered()
            return
        if file.endswith(".isd.json"):
            with open(file, mode="w+") as f:
                self.document.save(f, DocumentFormat.RAW)
        else:
            with open(file, mode="wb") as f:
                self.document.save(f)
        self.stbMain.showMessage(f"Saved to {self.file}.")

    def actSaveAs_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if not fileName:
            return
        fileName = os.path.realpath(fileName)
        if fileName.endswith(".isd.json"):
            with open(fileName, mode="w+") as f:
                self.document.save(f, DocumentFormat.RAW)
        else:
            with open(fileName, mode="wb") as f:
                self.document.save(f)
        self.file = fileName
        self.stbMain.showMessage(f"Saved to {self.file}.")

    def actOpen_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if fileName:
            fileName = os.path.realpath(fileName)
            if fileName.endswith(".isd.json"):
                with open(fileName, mode="r") as f:
                    doc = Document.load(f, DocumentFormat.RAW)
            else:
                with open(fileName, mode="rb") as f:
                    doc = Document.load(f)
            self.file = fileName
            self.document = doc
            self._freshAll()
            self.stbMain.showMessage(f"Opend document at {self.file}.")

    def actExport_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Export To", "",
            "PNG Image (*.png);; JPEG Image (*.jpeg);; BMP Image (*.bmp)",
            options=options)
        if fileName:
            fileName = os.path.realpath(fileName)
            ext = os.path.splitext(fileName)[1].lstrip(".")
            doc = self.document
            assert doc is not None
            context = NumpyArrayDrawingContext(
                NumpyArrayDrawingContext.create_array(doc.size))

            doc.drawings.render(context)

            Image.fromarray(context.array).save(fileName, ext, quality=95)

            self.stbMain.showMessage(f"Exported to {fileName}.")

    def editor_messaged(self, message: str) -> None:
        self.stbMain.showMessage(message)

    def editor_documentChanged(self, document: Document) -> None:
        self.document = document
        self._freshDockWidgets()

    def editor_stateChanged(self) -> None:
        self._freshActions()

    def editor_visual_stateChanged(self) -> None:
        self._freshActions()
