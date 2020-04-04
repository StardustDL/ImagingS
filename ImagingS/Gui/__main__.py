import sys

if __name__ == "__main__":
    from .app import Application
    app = Application(sys.argv)

    from .widgets import MainWindow

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.run())
