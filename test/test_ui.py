from PyQt5.QtWidgets import QMainWindow
from src.ui import MainWindow


def test_MainWindow(qtbot):
    window = QMainWindow()
    mui = MainWindow()
    mui.setupUi(window)
    window.show()
    qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
