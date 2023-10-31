import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from hexeditor import HexEditor
from connector import EditorConnector        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        # Create a layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Plain text"), 1, 1)
        layout.addWidget(QLabel("Hexa text"), 1, 2)

        self.clear_text = QTextEdit()
        self.hexa_text = HexEditor()

        self.connector=EditorConnector(self.clear_text,self.hexa_text)

        # Set line wrap mode to NoWrap
        self.clear_text.setLineWrapMode(QTextEdit.NoWrap)

        # Add horizontal scrollbar when needed
        self.clear_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        

        layout.addWidget(self.clear_text, 2, 1)
        layout.addWidget(self.hexa_text, 2, 2)

        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 2)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create the "Open" action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)

        # Add the "Open" action to the "File" menu
        file_menu.addAction(open_action)

        QShortcut(QKeySequence('Ctrl+O'), self).activated.connect(self.open_file)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setWindowTitle("Choose a file to open")
        filename, _ = dialog.getOpenFileName()

        if filename:
            with open(filename, "rb") as file:
                data = file.read()
                self.hexa_text.setBytes(data)
                self.clear_text.setText(data.decode())

                

app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Hex editor")
window.show()

app.exec()
