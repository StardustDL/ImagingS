import os
from enum import Enum, unique
from typing import Optional, cast

import qtawesome as qta
from PIL import Image
from PyQt5.QtGui import QCloseEvent, QKeySequence
from PyQt5.QtWidgets import (QAbstractItemView, QColorDialog, QDialog,
                             QFileDialog, QMainWindow, QMessageBox, QUndoStack)

import ImagingS.Gui.ui as ui
from ImagingS import Color
from ImagingS.brush import Brush, Brushes, SolidBrush
from ImagingS.document import Document, DocumentFormat, VersionController
from ImagingS.drawing import (Drawing, DrawingGroup, GeometryDrawing,
                              NumpyArrayRenderContext)
from ImagingS.Gui import icons
from ImagingS.Gui.models import (BrushModel, CommitCommand, DrawingModel,
                                 PropertyModel, TransformModel)
from ImagingS.transform import Transform, TransformGroup

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
        self.setupUndo()
        self.setupDockWidget()
        self.setupStatusBar()
        self.setupEditor()
        self.setupIcon()
        self._file = None
        self._document = None
        self.documentChanged = False

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actAbout.triggered.connect(self.actAbout_triggered)
        self.actQuit.triggered.connect(self.actQuit_triggered)
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
        self.modelDrawing.changed.connect(self.modelDrawing_changed)
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
        self.actTransformRemove.triggered.connect(
            self.actTransformRemove_triggered)
        self.actTransformClear.triggered.connect(
            self.actTransformClear_triggered)

        self.actBrushesRefresh.triggered.connect(
            self.actBrushesRefresh_triggered)
        self.actDrawingsRefresh.triggered.connect(
            self.actDrawingsRefresh_triggered)
        self.actTransformsRefresh.triggered.connect(
            self.actTransformsRefresh_triggered)
        self.actPropertiesRefresh.triggered.connect(
            self.actPropertiesRefresh_triggered)

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

        self.tabifyDockWidget(self.dwgBrushes, self.dwgDrawings)
        self.tabifyDockWidget(self.dwgBrushes, self.dwgTransforms)
        self.dwgDrawings.raise_()

        viewActions = [self.actToggleDrawings, self.actToggleBrushes,
                       self.actToggleTransforms, self.actToggleProperties]
        self.mnuView.addActions(viewActions)

    def setupUndo(self) -> None:
        self.versionController = VersionController()

        self.undoStack = QUndoStack(self)
        self.actUndo = self.undoStack.createUndoAction(self, "Undo")
        self.actUndo.setShortcut(QKeySequence.Undo)
        self.actRedo = self.undoStack.createRedoAction(self, "Redo")
        self.actRedo.setShortcut(QKeySequence.Redo)

        self.mnuEdit.addAction(self.actUndo)
        self.mnuEdit.addAction(self.actRedo)

    def setupStatusBar(self) -> None:
        pass

    def setupEditor(self) -> None:
        self.editor = DocumentEditor()
        self.editor.setObjectName("editor")
        self.gridLayout.addWidget(self.editor, 0, 0, 1, 1)
        self.editor.messaged.connect(self.editor_messaged)
        self.editor.documentCommitted.connect(self.editor_documentCommitted)
        self.editor.stateChanged.connect(self.editor_stateChanged)
        self.editor.visual.stateChanged.connect(self.editor_stateChanged)
        self.editor.code.stateChanged.connect(self.editor_stateChanged)

        self.mnuDrawing.addActions([
            self.editor.visual.actDrawingLine,
            self.editor.visual.actDrawingPolyline,
            self.editor.visual.actDrawingPolygon,
            self.editor.visual.actDrawingRectangle,
            self.editor.visual.actDrawingCurve,
            self.editor.visual.actDrawingEllipse,
        ])
        self.mnuDrawing.addSeparator()
        self.mnuDrawing.addActions([
            self.actDrawingRemove,
            self.actDrawingClear
        ])

        self.mnuTransform.addActions([
            self.editor.visual.actTransformTranslate,
            self.editor.visual.actTransformScale,
            self.editor.visual.actTransformRotate,
            self.editor.visual.actTransformSkew,
            self.editor.visual.actTransformMatrix,
            self.editor.visual.actTransformGroup,
        ])
        self.mnuTool.addActions([
            self.editor.visual.actClip
        ])
        self.mnuTransform.addSeparator()
        self.mnuTransform.addActions([
            self.actTransformRemove,
            self.actTransformClear
        ])

    def setupIcon(self):
        self.actNew.setIcon(qta.icon("mdi.file"))
        self.actOpen.setIcon(qta.icon("mdi.folder-open"))
        self.actSave.setIcon(qta.icon("mdi.content-save"))
        self.actSaveAs.setIcon(qta.icon("mdi.content-save-move"))
        self.actExport.setIcon(qta.icon("mdi.export"))
        self.actClose.setIcon(qta.icon("mdi.close"))
        self.actAbout.setIcon(qta.icon("mdi.information"))
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
        self.actDrawingsRefresh.setIcon(icons.refresh)
        self.actBrushesRefresh.setIcon(icons.refresh)
        self.actPropertiesRefresh.setIcon(icons.refresh)
        self.actTransformsRefresh.setIcon(icons.refresh)
        self.actToggleDrawings.setIcon(icons.drawing)
        self.actToggleBrushes.setIcon(icons.brush)
        self.actToggleProperties.setIcon(icons.property)
        self.actToggleTransforms.setIcon(icons.transform)
        self.actViewCode.setIcon(icons.code)
        self.actViewVisual.setIcon(icons.visual)
        self.setWindowIcon(qta.icon("mdi.pencil-box-multiple", color="purple"))

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.document is not None:
            self.actClose.trigger()
        if self.document is None:
            event.accept()
        else:
            event.ignore()

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

    @property
    def documentChanged(self) -> bool:
        return self._documentChanged

    @documentChanged.setter
    def documentChanged(self, value: bool) -> None:
        self._documentChanged = value
        self._freshTitle()

    def _freshTitle(self) -> None:
        if self.file is None:
            if self.document is None:
                self.setWindowTitle("ImagingS")
            else:
                if self.documentChanged:
                    self.setWindowTitle("Untitled * - ImagingS")
                else:
                    self.setWindowTitle("Untitled - ImagingS")
        else:
            if self.documentChanged:
                self.setWindowTitle(f"{self.file} * - ImagingS")
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

    def _freshTransforms(self):
        drawing = self._currentDrawing()
        hasDrawing = drawing is not None
        self.dwgTransforms.setEnabled(hasDrawing)
        trans = None
        if hasDrawing:
            if isinstance(drawing, GeometryDrawing):
                trans = drawing.geometry.transform
            elif isinstance(drawing, DrawingGroup):
                trans = drawing.transform
        self.modelTransform.fresh(trans)
        if trans is not None:
            self.trvTransforms.expandAll()

    def _freshProperties(self):
        hasDoc = self.document is not None
        self.modelProperties.fresh()
        self.dwgProperties.setEnabled(hasDoc)

    def _freshDockWidgets(self):
        self._freshProperties()
        self._freshBrushes()
        self._freshDrawings()
        self._freshTransforms()

    def _freshActions(self):
        hasDoc = self.document is not None

        self.actClose.setEnabled(hasDoc)
        self.actSave.setEnabled(hasDoc)
        self.actSaveAs.setEnabled(hasDoc)
        self.actExport.setEnabled(hasDoc)
        self.actNew.setEnabled(not hasDoc)

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

        if isVisualNormal:
            tri = cast(QAbstractItemView.EditTriggers,
                       QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
            self.trvTransforms.setEditTriggers(tri)
            self.trvBrushes.setEditTriggers(tri)
            self.trvDrawings.setEditTriggers(tri)
            self.trvProperties.setEditTriggers(tri)
        else:
            self.trvTransforms.setEditTriggers(
                QAbstractItemView.NoEditTriggers)
            self.trvBrushes.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.trvDrawings.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.trvProperties.setEditTriggers(
                QAbstractItemView.NoEditTriggers)

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

    def _commitDocument(self, message: str):
        assert self.document is not None
        self.documentChanged = True
        cmt = self.versionController.commit(self.document, message)
        self.undoStack.push(CommitCommand(
            cmt, self.versionController, self.undoCallback))

    def _currentDrawing(self) -> Optional[Drawing]:
        indexs = self.trvDrawings.selectedIndexes()
        if len(indexs) == 0:
            return None
        return self.modelDrawing.getUserData(indexs[0])

    def _currentBrush(self) -> Optional[Brush]:
        indexs = self.trvBrushes.selectedIndexes()
        if len(indexs) == 0:
            return None
        return self.modelBrush.getUserData(indexs[0])

    def _currentTransform(self) -> Optional[Transform]:
        indexs = self.trvTransforms.selectedIndexes()
        if len(indexs) == 0:
            return None
        return self.modelTransform.getUserData(indexs[0])

    def trvBrushes_clicked(self, index):
        item = self.modelBrush.getUserData(index)
        if self.modelProperties.obj is not item:
            self.editor.visual.brush = item
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.trvBrushes.clearSelection()
            self.editor.visual.brush = None
            self.modelProperties.fresh()

    def trvDrawings_clicked(self, index):
        item = self.modelDrawing.getUserData(index)
        if item is not self.document.drawings and self.modelProperties.obj is not item:
            self.editor.visual.drawing = item
            self._freshTransforms()
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.trvDrawings.clearSelection()
            self.editor.visual.drawing = None
            self._freshTransforms()
            self.modelProperties.fresh()

    def trvTransforms_clicked(self, index):
        item = self.modelTransform.getUserData(index)
        if self.modelProperties.obj is not item:
            self.modelProperties.fresh(item)
            self.trvProperties.expandAll()
        else:
            self.trvTransforms.clearSelection()
            self.modelProperties.fresh()

    def actViewVisual_triggered(self):
        self.editor.switchVisual()

    def actViewCode_triggered(self):
        self.editor.switchCode()

    def actDrawingRemove_triggered(self):
        item = self._currentDrawing()
        if item is None:
            return
        parent = item.parent()
        if parent is None:
            return
        del parent[item.id]
        self._commitDocument(f"Deleted drawing ({item}).")
        self._freshDrawings()
        self.editor.fresh()
        self.stbMain.showMessage(f"Deleted drawing ({item}).")

    def actDrawingClear_triggered(self):
        self.document.drawings.children.clear()
        self._commitDocument("Cleared drawings")
        self._freshDrawings()
        self.editor.fresh()
        self.stbMain.showMessage("Cleared drawings.")

    def actBrushSolid_triggered(self):
        assert self.document is not None
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        br = SolidBrush(Color(
            color.red(), color.green(), color.blue()))
        self.document.brushes.append(br)
        self._commitDocument("Create SolidBrush")
        self._freshBrushes()
        self.stbMain.showMessage(
            f"Add new brush ({br}).")

    def actBrushRemove_triggered(self):
        item = self._currentBrush()
        if item is None:
            return
        parent = item.parent()
        if parent is None:
            return
        del parent[item.id]
        self._commitDocument(f"Deleted brush ({item})")
        self._freshBrushes()
        self.stbMain.showMessage(
            f"Deleted brush ({item}).")

    def actBrushClear_triggered(self):
        self.document.brushes.clear()
        self._commitDocument("Cleared brushes")
        self._freshBrushes()
        self.stbMain.showMessage("Cleared brushes.")

    def actTransformRemove_triggered(self):
        item = self._currentTransform()
        if item is None:
            return
        drawing = self._currentDrawing()
        if isinstance(drawing, GeometryDrawing):
            if item == drawing.geometry.transform:
                drawing.geometry.transform = None
            else:
                parent = item.parent()
                if parent is None:
                    return
                del parent[item.id]
        elif isinstance(drawing, DrawingGroup):
            if item == drawing.transform:
                drawing.transform = None
            elif isinstance(drawing.transform, TransformGroup):
                parent = item.parent()
                if parent is None:
                    return
                del parent[item.id]
        self._commitDocument(f"Deleted transform ({item})")
        self._freshTransforms()
        self.editor.fresh()
        self.stbMain.showMessage(
            f"Deleted transform ({item}).")

    def actTransformClear_triggered(self):
        drawing = self._currentDrawing()
        if drawing is None:
            return
        if isinstance(drawing, GeometryDrawing):
            if isinstance(drawing.geometry.transform, TransformGroup):
                drawing.geometry.transform.children.clear()
            else:
                drawing.geometry.transform = None
        elif isinstance(drawing, DrawingGroup):
            if isinstance(drawing.transform, TransformGroup):
                drawing.transform.children.clear()
            else:
                drawing.transform = None
        self._commitDocument("Cleared transforms")
        self._freshTransforms()
        self.editor.fresh()
        self.stbMain.showMessage("Cleared transforms.")

    def actClose_triggered(self):
        if self.documentChanged:
            code = QMessageBox.warning(self, "Unsaved changes", "Do you want save changes?",
                                       cast(QMessageBox.StandardButtons, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel), QMessageBox.Yes)
            if code == QMessageBox.Cancel:
                return
            elif code == QMessageBox.Yes:
                self.actSave.trigger()
        self.undoStack.clear()
        self.versionController.clear()
        self.document = None
        self.documentChanged = False
        self.file = None
        self._freshAll()

    def actNew_triggered(self):
        newDialog = NewDocumentDialog()
        if newDialog.exec_() == QDialog.Accepted:
            doc = Document()
            doc.brushes.append(Brushes.Black)
            doc.size = newDialog.documentSize
            self.document = doc
            self.documentChanged = True
            self.versionController.commit(self.document, "Initial")
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
        self.documentChanged = False
        self.stbMain.showMessage(f"Saved to {self.file}.")

    def actSaveAs_triggered(self):
        options = QFileDialog.Options()
        fileName, okPressed = QFileDialog.getSaveFileName(
            self, "Save As", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if not okPressed or not fileName:
            return
        fileName = os.path.realpath(fileName)
        self.file = fileName
        self.actSave.trigger()

    def actOpen_triggered(self):
        options = QFileDialog.Options()
        fileName, okPressed = QFileDialog.getOpenFileName(
            self, "Open", "", "ImagingS Document (*.isd);; ImagingS Raw Document (*.isd.json)", options=options)
        if not okPressed or not fileName:
            return
        fileName = os.path.realpath(fileName)
        if fileName.endswith(".isd.json"):
            with open(fileName, mode="r") as f:
                doc = Document.load(f, DocumentFormat.RAW)
        else:
            with open(fileName, mode="rb") as f:
                doc = Document.load(f)
        self.file = fileName
        self.document = doc
        self.documentChanged = False
        self.versionController.commit(self.document, "Initial")
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
            context = NumpyArrayRenderContext(
                NumpyArrayRenderContext.create_array(doc.size))

            doc.drawings.render(context)

            Image.fromarray(context.array).save(fileName, ext, quality=95)

            self.stbMain.showMessage(f"Exported to {fileName}.")

    def actAbout_triggered(self) -> None:
        QMessageBox.information(self, "About ImagingS", """
Author    StardustDL
Project   https://github.com/StardustDL/ImagingS
License   MPL-2.0
""".strip())

    def actQuit_triggered(self) -> None:
        self.close()

    def actBrushesRefresh_triggered(self) -> None:
        self._freshBrushes()

    def actDrawingsRefresh_triggered(self) -> None:
        self._freshDrawings()

    def actTransformsRefresh_triggered(self) -> None:
        self._freshTransforms()

    def actPropertiesRefresh_triggered(self) -> None:
        self.modelProperties.fresh(self.modelProperties.obj)

    def editor_messaged(self, message: str) -> None:
        self.stbMain.showMessage(message)

    def editor_documentCommitted(self, document: Document, message: str) -> None:
        self.document = document
        self._commitDocument(message)
        self._freshDockWidgets()

    def undoCallback(self, document: Document) -> None:
        self.document = document
        self._freshAll()

    def editor_stateChanged(self) -> None:
        if self.editor.state is DocumentEditorState.Visual:
            self.actViewCode.setChecked(False)
            self.actViewVisual.setChecked(True)
        elif self.editor.state is DocumentEditorState.Code:
            self.actViewCode.setChecked(True)
            self.actViewVisual.setChecked(False)

        self._freshActions()

    def modelDrawing_changed(self) -> None:
        self._freshDrawings()
