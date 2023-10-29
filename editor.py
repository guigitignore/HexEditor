import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class CustomReadOnlyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.cursor=self.textCursor()

    def mousePressEvent(self, event:QMouseEvent):
        self.cursor.setCharFormat(QTextCharFormat())
        cursor = self.cursorForPosition(event.position().toPoint())
        
        line = cursor.blockNumber()  # Line number is 1-based
        column = cursor.columnNumber()  # Column number is 1-based
        print(f"Clicked at Line {line}, Column {column}")

        nchar=column%3
        if nchar!=2:
            self.highlight_text(line,column-nchar,line,column-nchar+2)


        super().mousePressEvent(event)

    def highlight_text(self,start_line,start_column,end_line,end_column):
        start_pos = self.textCursor().document().findBlockByLineNumber(start_line).position() + start_column 
        end_pos = self.textCursor().document().findBlockByLineNumber(end_line).position() + end_column 

        cursor = self.textCursor()
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        
        format = QTextCharFormat()
        format.setBackground(Qt.yellow)
        cursor.setCharFormat(format)
        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        # Create a layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Plain text"), 1, 1)
        layout.addWidget(QLabel("Hexa text"), 1, 2)

        self.clear_text = QTextEdit()
        self.hexa_text = CustomReadOnlyTextEdit()

        # Set line wrap mode to NoWrap
        self.clear_text.setLineWrapMode(QTextEdit.NoWrap)
        self.hexa_text.setLineWrapMode(QTextEdit.NoWrap)

        # Add horizontal scrollbar when needed
        self.clear_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.hexa_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

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
                binary_lines = file.read().split(b'\n')

                for binary_line in binary_lines:
                    hex_line=" ".join([format(byte,'x') for byte in binary_line])
                    clear_line=binary_line.decode("utf-8") 

                    self.clear_text.append(clear_line)
                    self.hexa_text.append(hex_line)
                

app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Hex editor")
window.show()

app.exec()
