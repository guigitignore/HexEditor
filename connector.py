from hexeditor import HexEditor
from PySide6.QtWidgets import QTextEdit


class EditorConnector:

    def __init__(self,plain_text:QTextEdit,hex_text:HexEditor) -> None:
        self.plain_text:QTextEdit=plain_text
        self.hex_text:HexEditor=hex_text
        self.plain_text.cursorPositionChanged.connect(self.plainTextPositionChanged)
        
        #self.hex_text.cursorPositionChanged.connect(self.hexTextPositionChanged)

    def plainTextPositionChanged(self):
        position=self.plain_text.textCursor().position()
        cursor=self.hex_text.textCursor()
        self.hex_text.verticalSrollbar.setSliderPosition((position*3 /self.hex_text.document().characterCount())*self.hex_text.verticalSrollbar.maximum())
        cursor.setPosition(position*3)
        print(f"plaintext {position}")
        self.hex_text.setTextCursor(cursor)

    def hexTextPositionChanged(self):
        position=self.hex_text.textCursor().position()
        cursor=self.plain_text.textCursor()
        cursor.setPosition(position//3)
        print(f"hextext {position}")
        self.plain_text.setTextCursor(cursor)