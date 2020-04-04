from ImagingS.Gui.widgets import MainWindow
from ImagingS.Gui.app import Application


def test_MainWindow(qtbot) -> None:
    Application([])

    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
