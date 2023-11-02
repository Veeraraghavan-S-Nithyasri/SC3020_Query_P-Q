# interface.py

''' Simple interface testing: installation of pyqt6 is required. '''

import sys
from PyQt6.QtWidgets import ( QApplication, QLabel, QWidget, QMainWindow, QStatusBar, QToolBar,
                             QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QPlainTextEdit, QTextEdit
                             
)
from PyQt6.QtGui import *
from PyQt6.QtCore import *


# enumerations
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 750
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 25
TEXTBOX_WIDTH = WINDOW_WIDTH - 20
TEXTBOX_HEIGHT = 120

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
class DBInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SC3020 Project 2")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(10,10,10,10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.initTitle(layout)
        self.initQueryInput(layout)
        layout.addStretch(10)
        self.diskBlockOutput(layout)
        layout.addStretch(10)
        self.qepOutput(layout)
        layout.addStretch(10)
        self.resetButton(layout)
        self.setLayout(layout)

    # initialize title block
    def initTitle(self, layout):
        self.winTitle = QLabel("<h1>SC3020 Project 2</h1>\n")
        self.winTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.windowdesc = QLabel("This interface demonstrates visual exploration of SQL query exploration.\n")
        #windowdesc2 = QLabel("Test")

        layout.addWidget(self.winTitle)
        layout.addStretch(0)
        layout.addWidget(self.windowdesc)

    # SQL query input box
    def initQueryInput(self, layout):
        self.header1 = QLabel("<h2>SQL query input:</h2>\n")
        self.desc1 = QLabel("Input your SQL query into the text box below.\n")
        self.inputBox = QPlainTextEdit()
        #inputBox.insertPlainText("Key in your SQL query here.\n")
        self.inputBox.setFixedSize(TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        self.button1 = QPushButton("Execute Query")
        self.button1.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)


        layout.addWidget(self.header1)
        layout.addStretch(0)
        layout.addWidget(self.desc1)
        layout.addStretch(0)
        layout.addWidget(self.inputBox)
        layout.addStretch(10)
        layout.addWidget(self.button1)

    # Disk block access display
    def diskBlockOutput(self, layout):
        self.header2 = QLabel("<h2>Disk blocks accessed for data output:</h2>\n")
        self.desc2 = QLabel("Overview of disk blocks accessed will be displayed here.\n")
        self.displayBox1 = QTextEdit("Empty\n")
        #QTextEdit is temporary for now, may or may not change depending on how we choose to display the results.
        self.displayBox1.setFixedSize(TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        self.displayBox1.setReadOnly(True)

        layout.addWidget(self.header2)
        layout.addStretch(0)
        layout.addWidget(self.desc2)
        layout.addStretch(0)
        layout.addWidget(self.displayBox1)

    # QEP display
    def qepOutput(self, layout):
        self.header3 = QLabel("<h2>Query execution plan:</h2>\n")
        self.desc3 = QLabel("Detailed query execution plan will be displayed here.\n")
        self.displayBox2 = QTextEdit("Empty\n")
        #QTextEdit is temporary for now, may or may not change depending on how we choose to display the results.
        self.displayBox2.setFixedSize(TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        self.displayBox2.setReadOnly(True)

        layout.addWidget(self.header3)
        layout.addStretch(0)
        layout.addWidget(self.desc3)
        layout.addStretch(0)
        layout.addWidget(self.displayBox2)

    # set disk block output display
    def setDiskBlockOutput(self, text):
        self.displayBox1.setText(text)

    # set QEP display
    def setQEPOutput(self, text):
        self.displayBox2.setText(text)

    # reset button
    def resetButton(self, layout):
        self.resetB = QPushButton("Reset All")
        self.resetB.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.resetB.clicked.connect(self.resetFields)
        layout.addWidget(self.resetB)

    # reset all fields
    def resetFields(self):
        self.inputBox.setPlainText("")
        self.displayBox1.setText("Empty\n")
        self.displayBox2.setText("Empty\n")
        


# define main function
def main():
    app = QApplication([])
    gui_window = DBInterface()
    gui_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()