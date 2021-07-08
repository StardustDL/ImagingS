import sys


def main():
    from .app import Application
    app = Application(sys.argv)

    from .widgets import MainWindow

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
