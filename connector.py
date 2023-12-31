from hexeditor import HexEditor
from PySide6.QtWidgets import QTextEdit
from plaintexteditor import PlainTextEditor

class EditorConnector:

    def __init__(self,plain_text:PlainTextEditor,hex_text:HexEditor) -> None:
        self.plain_text:PlainTextEditor=plain_text
        self.hex_text:HexEditor=hex_text

        self.plain_text.textChanged.connect(self.plainTextChanged)
        self.hex_text.textChanged.connect(self.hexTextChanged)

        self.plain_text.verticalScrollBar().valueChanged.connect(self.syncScrollbars)
        self.hex_text.verticalScrollBar().valueChanged.connect(self.syncScroll)

        #self.plain_text.cursorPositionChanged.connect(self.plainTextPositionChanged)
        #self.hex_text.cursorPositionChanged.connect(self.hexTextPositionChanged)

        self.text_updating=False
        self.cursor_updating=False
        self.scroll_updating=False

    def syncScrollbars(self):
        if not self.scroll_updating:
            self.scroll_updating=True
            value = self.plain_text.verticalScrollBar().value()
            self.hex_text.verticalScrollBar().setValue(value)
            self.scroll_updating=False

    def syncScroll(self,dy):
        if not self.scroll_updating:
            self.scroll_updating=True
            value = self.hex_text.verticalScrollBar().value()
            self.plain_text.verticalScrollBar().setValue(value)
            self.scroll_updating=False

    def plainTextChanged(self):
        if not self.text_updating:
            self.text_updating=True
            #print("update hex text")
            self.hex_text.updateBytes()
            self.text_updating=False

    def hexTextChanged(self):
        if not self.text_updating:
            self.text_updating=True
            #print("update plain text")
            self.plain_text.updateBytes()
            self.text_updating=False


    def plainTextPositionChanged(self):
        if not self.cursor_updating:
            self.cursor_updating=True

            position=self.plain_text.textCursor().position()
            cursor=self.hex_text.textCursor()
           
            cursor.setPosition(position*3)
            self.hex_text.setTextCursor(cursor)

            self.cursor_updating=False

    def hexTextPositionChanged(self):
        if not self.cursor_updating:
            self.cursor_updating=True

            position=self.hex_text.textCursor().position()
            cursor=self.plain_text.textCursor()
            cursor.setPosition(position//3)
            self.plain_text.setTextCursor(cursor)

            self.cursor_updating=False