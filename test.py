import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create the central widget
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Create two QTextEdit widgets
        self.lowerTextEdit = QTextEdit()
        self.upperTextEdit = QTextEdit()

        # Set text formats to enforce lower/upper case
        self.lowerTextEdit.setPlaceholderText("Lowercase text only")
        self.lowerTextEdit.setAcceptRichText(False)
        self.lowerTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.lowerTextEdit.setPlainText("")

        self.upperTextEdit.setPlaceholderText("Uppercase text only")
        self.upperTextEdit.setAcceptRichText(False)
        self.upperTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.upperTextEdit.setPlainText("")

        # Connect textChanged signal to slot
        self.lowerTextEdit.textChanged.connect(self.updateUpperTextEdit)
        self.upperTextEdit.textChanged.connect(self.updateLowerTextEdit)

        layout.addWidget(self.lowerTextEdit)
        layout.addWidget(self.upperTextEdit)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.updating = False  # Add a flag to prevent infinite loop

    def updateUpperTextEdit(self):
        if not self.updating:
            self.updating = True
            lower_text = self.lowerTextEdit.toPlainText()
            upper_text = lower_text.upper()
            self.upperTextEdit.setPlainText(upper_text)
            self.updating = False

    def updateLowerTextEdit(self):
        if not self.updating:
            self.updating = True
            upper_text = self.upperTextEdit.toPlainText()
            lower_text = upper_text.lower()
            self.lowerTextEdit.setPlainText(lower_text)
            self.updating = False

def main():
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
