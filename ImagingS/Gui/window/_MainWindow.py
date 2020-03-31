import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color, brush
from ImagingS.Gui.models import BrushModel

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QInputDialog, QLineEdit, QMessageBox


class MainWindow(QMainWindow, ui.MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
