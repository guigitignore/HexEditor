from hexeditor import HexEditor
from PySide6.QtWidgets import QTextEdit


class EditorConnector:

    def __init__(self,plain_text:QTextEdit,hex_text:HexEditor) -> None:
        self.plain_text:QTextEdit=plain_text
        self.hex_text:HexEditor=hex_text

        self.plain_text.textChanged.connect(self.plainTextChanged)
        self.hex_text.textChanged.connect(self.hexTextChanged)

        self.plain_text.cursorPositionChanged.connect(self.plainTextPositionChanged)
        self.hex_text.cursorPositionChanged.connect(self.hexTextPositionChanged)

        self.text_updating=False
        self.cursor_updating=False

    def plainTextChanged(self):
        if not self.text_updating:
            self.text_updating=True

            try:
                self.hex_text.setBytes(self.plain_text.toPlainText().encode())
            finally:
                self.text_updating=False

    def hexTextChanged(self):
        if not self.text_updating:
            self.text_updating=True

            try:
                self.plain_text.setText(bytes.fromhex(self.hex_text.toPlainText()).decode(errors="replace"))
            finally:
                self.text_updating=False


    def plainTextPositionChanged(self):
        if not self.cursor_updating:
            self.cursor_updating=True

            position=self.plain_text.textCursor().position()
            cursor=self.hex_text.textCursor()
            self.hex_text.verticalSrollbar.setSliderPosition((position*3 /self.hex_text.document().characterCount())*self.hex_text.verticalSrollbar.maximum())
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