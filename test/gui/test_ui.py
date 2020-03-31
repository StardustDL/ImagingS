from PyQt5.QtWidgets import QMainWindow
from ImagingS.Gui.ui import MainWindow


def test_MainWindow(qtbot) -> None:
    window = QMainWindow()
    mui = MainWindow()
    mui.setupUi(window)
    window.show()
    # qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
