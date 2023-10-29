from __future__ import annotations
from PySide6.QtCore import Slot, Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QTextFormat
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit



class LineNumberArea(QWidget):
    def __init__(self, editor:HexEditor):
        QWidget.__init__(self, editor)
        self.editor:HexEditor = editor
        self.setFont(self.editor.font())
        self.move(0,self.editor.columnNumberArea().getHeight())

    def sizeHint(self):
        return QSize(self.getWidth(), self.getHeight())
    
    def charNeeded(self):
        return len(format((self.editor.blockCount()-1)<<4,"X"))
    
    def getWidth(self):
        return self.editor.fontMetrics().horizontalAdvance('A') * self.charNeeded()
    
    def getHeight(self):
        return self.editor.viewport().height()

    
    def paintEvent(self, event):
        #print(f"paintevent {self.width()}")
        
        painter = QPainter(self)
        
        painter.fillRect(event.rect(), Qt.red)
    

        hexformat="0{}X".format(self.charNeeded())

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()<<4
        offset = self.editor.contentOffset()

        top = self.editor.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = format(block_number,hexformat)
                painter.setPen(Qt.black)
                
                width = self.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width, height, Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 16

        painter.end()

    


class ColumnNumberArea(QWidget):
    def __init__(self, editor:HexEditor):
        QWidget.__init__(self, editor)
        self.editor:HexEditor = editor
        self._text=" ".join([format(i,"02X") for i in range(16)])
        self._textWidth=self.editor.viewport().fontMetrics().horizontalAdvance(self._text)
        
    def paintEvent(self, event):
        painter=QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        painter.setPen(Qt.black)
        
        painter.drawText(0, 0, self._textWidth, self.height(), Qt.AlignLeft, self._text)
        painter.end()

    def sizeHint(self):
        return QSize(self.getWidth(), self.getHeight())
    
    def getWidth(self):
        return self._textWidth
    
    def getHeight(self):
        return self.editor.fontMetrics().height()+3


class HexEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.column_number_area= ColumnNumberArea(self)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.update_line_number_area_width()

    def lineNumberArea(self):
        return self.line_number_area
    

    def columnNumberArea(self):
        return self.column_number_area
    
    @Slot()
    def update_line_number_area_width(self, _=None):
        width=self.line_number_area.getWidth()
        self.column_number_area.move(width,0)
        self.setFixedWidth(width+self.column_number_area.getWidth())
        self.setViewportMargins(width, self.column_number_area.getHeight(), 0,0)
        if width!=self.line_number_area.width():
            self.line_number_area.resize(width,self.line_number_area.getHeight())
        else:
            self.line_number_area.update()

    @Slot()
    def update_line_number_area(self, rect, dy):
        #print("update_line_number_area")
        if dy:
            self.line_number_area.scroll(0, dy)


import sys
from PySide6.QtWidgets import QApplication

"""PySide6 port of the widgets/codeeditor example from Qt5"""

if __name__ == "__main__":
    app = QApplication([])
    editor = HexEditor()
    editor.setWindowTitle("Code Editor Example")
    editor.show()
    sys.exit(app.exec())



