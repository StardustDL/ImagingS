from ImagingS.Gui.app import Application


def test_mainWindow(qtbot) -> None:
    Application([])

    from ImagingS.Gui.widgets import MainWindow

    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    assert window.windowTitle() == "ImagingS"
