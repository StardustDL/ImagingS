import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color, brush
from ImagingS.Gui.models import BrushModel
import qtawesome as qta

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QInputDialog, QLineEdit, QMessageBox


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setupIcon()

        self.actClose.triggered.connect(self.actClose_triggered)
        self.actQuit.triggered.connect(self.close)
        self.actNew.triggered.connect(self.actNew_triggered)
        self.actSave.triggered.connect(self.actSave_triggered)
        self.actOpen.triggered.connect(self.actOpen_triggered)
        self.actDrawings.triggered.connect(self.actDrawings_triggered)
        self.actProperties.triggered.connect(self.actProperties_triggered)
        self.actBrushes.triggered.connect(self.actBrushes_triggered)
        self.actBrushSolid.triggered.connect(self.actBrushSolid_triggered)

        self.modelBrush = BrushModel(self)
        self.trvBrushes.setModel(self.modelBrush)

        Application.current().documentChanged.connect(self.app_documentChanged)
        self.actNew.trigger()

    def setupIcon(self):
        self.actNew.setIcon(qta.icon("mdi.file"))
        self.actOpen.setIcon(qta.icon("mdi.folder-open"))
        self.actSave.setIcon(qta.icon("mdi.content-save"))
        self.actExport.setIcon(qta.icon("mdi.export"))
        self.actClose.setIcon(qta.icon("mdi.close"))
        self.actQuit.setIcon(qta.icon("mdi.exit-to-app"))
        self.actUndo.setIcon(qta.icon("mdi.undo"))
        self.actRedo.setIcon(qta.icon("mdi.redo"))
        self.actDrawings.setIcon(qta.icon("mdi.drawing"))
        self.actBrushes.setIcon(qta.icon("mdi.brush"))
        self.actProperties.setIcon(qta.icon("mdi.database"))
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
        self.actBrushRemove.setIcon(qta.icon("mdi.delete"))
        self.actDrawingRemove.setIcon(qta.icon("mdi.delete"))
        self.actBrushClear.setIcon(qta.icon("mdi.delete-sweep"))
        self.actDrawingClear.setIcon(qta.icon("mdi.delete-sweep"))
        self.dwgBrushes.setWindowIcon(qta.icon("mdi.brush"))
        self.dwgDrawings.setWindowIcon(qta.icon("mdi.drawing"))
        self.dwgProperties.setWindowIcon(qta.icon("mdi.database"))
        self.setWindowIcon(qta.icon("mdi.pencil-box-multiple"))

    def app_documentChanged(self):
        doc = Application.current().document
        hasDoc = doc is not None
        self.actClose.setEnabled(hasDoc)
        self.gvwMain.setEnabled(hasDoc)
        self.mnuDrawing.setEnabled(hasDoc)
        self.mnuTransform.setEnabled(hasDoc)
        self.mnuBrush.setEnabled(hasDoc)
        self.trvDrawings.setEnabled(hasDoc)
        self.trvBrushes.setEnabled(hasDoc)
        self.trvProperties.setEnabled(hasDoc)

        if hasDoc:
            self.modelBrush.clear_items()
            for br in doc.brushes:
                self.modelBrush.append(br)

    def actBrushes_triggered(self):
        if self.actBrushes.isChecked():
            self.dwgBrushes.show()
        else:
            self.dwgBrushes.hide()

    def actProperties_triggered(self):
        if self.actProperties.isChecked():
            self.dwgProperties.show()
        else:
            self.dwgProperties.hide()

    def actDrawings_triggered(self):
        if self.actDrawings.isChecked():
            self.dwgDrawings.show()
        else:
            self.dwgDrawings.hide()

    def actBrushSolid_triggered(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        name = None
        while name is None:
            name, ok = QInputDialog.getText(
                self, "Input Name", "Brush Name:", QLineEdit.Normal, "")
            if ok:
                if not name or Application.current().document.brushes.contains(name):
                    QMessageBox.question(
                        self, "Invalid Name", "The name is empty or it exists. Please input name again.", QMessageBox.Retry, QMessageBox.Retry)
                    name = None
            else:
                name = None
                break

        if name is None:
            return

        br = brush.Solid(Color(color.red(), color.green(), color.blue()))
        br.id = name
        Application.current().document.brushes.append(br)
        self.modelBrush.append(br)

    def actClose_triggered(self):
        Application.current().document = None

    def actNew_triggered(self):
        Application.current().document = Document()

    def actSave_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save as", "", "ImagingS document (*.isd.json)", options=options)
        if fileName:
            with open(fileName, mode="w+") as f:
                Application.current().document.save(f)

    def actOpen_triggered(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "", "ImagingS document (*.isd.json)", options=options)
        if fileName:
            with open(fileName, mode="r") as f:
                Application.current().document = Document.load(f)
