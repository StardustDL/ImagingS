from ImagingS.Gui.app import Application


def test_MainWindow(qtbot) -> None:
    Application([])

    from ImagingS.Gui.widgets import MainWindow

    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
