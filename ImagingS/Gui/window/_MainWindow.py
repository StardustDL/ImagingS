import ImagingS.Gui.ui as ui
from ImagingS.document import Document
from ImagingS.Gui.app import Application
from ImagingS.core import Color, brush

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog


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
        Application.current().documentChanged.connect(self.app_documentChanged)
        self.app_documentChanged()

    def app_documentChanged(self):
        hasDoc = Application.current().document is not None
        self.actClose.setEnabled(hasDoc)
        self.gvwMain.setEnabled(hasDoc)
        self.mnuDrawing.setEnabled(hasDoc)
        self.mnuTransform.setEnabled(hasDoc)
        self.mnuBrush.setEnabled(hasDoc)

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
        br = brush.Solid(Color(color.red(), color.green(), color.blue()))
        Application.current().document.brushes.append(br)

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
