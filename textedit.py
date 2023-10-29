import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor,QKeyEvent

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.text=[bytearray()]
        self.cursor:QTextCursor=self.textCursor()

    def addText(self,content:list[bytearray]):
        last=content.pop()
        for line in content:
            self.appendContent(line)
            self.appendLine()
        self.appendContent(last)
        

    def appendContent(self,content:bytearray):
        self.append(' '.join([format(b,'02X') for b in content]))
        self.text[-1].extend(content)

    def appendLine(self):
        self.append('\n')
        self.text.append(bytearray())
        

    def keyPressEvent(self, event:QKeyEvent):
        #print(self.textCursor().positionInBlock())
        key=event.text().capitalize()

        if event.key()==Qt.Key_Insert:
            print("insert")

        if event.key()==Qt.Key_Delete:
            print("suppr")
        

        if key in "0123456789ABCDEF":
            self.insertPlainText(key)

        if event.key() == Qt.Key_Backspace:
            # Customize behavior for Backspace key
            # For example, don't allow backspace to delete content
            cursor = self.textCursor()
            
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 3)
            cursor.removeSelectedText()
            return
            
        if event.key() in [Qt.Key_Left,Qt.Key_Right,Qt.Key_Up,Qt.Key_Down]:
            super().keyPressEvent(event)
        

        # Handle other key events here
        #super().keyPressEvent(event)

    def insertFromMimeData(self, source):
        # Customize behavior when pasting content
        # For example, ignore pasted content
        return

def formattext(b:bytes)->list[bytearray]:
    return [bytearray(l) for l in b.split(b'\n')]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        text_edit = CustomTextEdit()
        text_edit.addText(formattext(bytes("test",'utf-8')))
        self.setCentralWidget(text_edit)




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


