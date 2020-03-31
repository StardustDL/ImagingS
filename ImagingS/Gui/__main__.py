import sys
from .app import Application
from .window import MainWindow

if __name__ == "__main__":
    app = Application(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.run())
