# interface.py

''' Simple interface testing: installation of pyqt6 is required. '''

import sys
from PyQt6.QtWidgets import ( QApplication, QLabel, QWidget, QMainWindow, QStatusBar, QToolBar,
                             QPushButton, QGridLayout, QVBoxLayout, QLineEdit
                             
)

# enumerations
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 40

# # app instance
# app = QApplication([])

# # app GUI
# window = QWidget()
# window.setWindowTitle("SC3020 Project 2")
# window.setGeometry(100, 100, 800, 600)
# helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
# helloMsg.move(320, 15)


# # show app GUI
# window.show()


# # terminate program
# sys.exit(app.exec())

# interface class definition
class DBInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SC3020 Project 2")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        centralWidget = QWidget(self)
        windowTitle = QLabel("<h1>Hello, World!</h1>", parent=centralWidget)
        windowTitle.move(320, 15)
        #centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)


# define main function
def main():
    app = QApplication([])
    gui_window = DBInterface()
    gui_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()