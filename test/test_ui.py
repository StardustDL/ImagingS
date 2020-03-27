from PyQt5.QtWidgets import QMainWindow
from src.ui import MainWindow
from . import is_linux


def test_MainWindow(qtbot):
    window = QMainWindow()
    mui = MainWindow()
    mui.setupUi(window)
    if not is_linux:
        window.show()
    # qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
