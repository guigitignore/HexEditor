from __future__ import annotations
from PySide6.QtWidgets import QTextEdit,QWidget,QScrollBar
from PySide6.QtGui import QPainter,QKeyEvent,QResizeEvent,QTextCursor,QTextCharFormat,QColor,QMouseEvent
from PySide6.QtCore import QSize,Qt,Slot,Signal


class PlainTextEditor(QTextEdit):

    class ColumnNumberArea(QWidget):
        def __init__(self, editor:QTextEdit):
            QWidget.__init__(self, editor)
            self.editor:QTextEdit = editor
            self._text="".join([format(i,"X") for i in range(16)])
            self._textWidth=self.editor.viewport().fontMetrics().horizontalAdvance(self._text)
            
        def paintEvent(self, event):
            painter=QPainter(self)
            painter.fillRect(event.rect(), Qt.lightGray)
            painter.setPen(Qt.black)
            painter.setFont(self.editor.font())
            
            painter.drawText(0, 0, self._textWidth, self.height(), Qt.AlignLeft, self._text)
            painter.end()

        def characterCount(self):
            return len(self._text)

        def sizeHint(self):
            return QSize(self.getWidth(), self.getHeight())
        
        def getWidth(self):
            return self._textWidth
        
        def getHeight(self):
            return self.editor.fontMetrics().height()+3
    
        

    def __init__(self):
        super().__init__()

        # Set a monospaced font
        monospaced_font = self.font()
        monospaced_font.setFamily("Courier New")
        monospaced_font.setFixedPitch(True)
        monospaced_font.setPointSize(12)
        self.setFont(monospaced_font)

        # Set a fixed width for the widget
        self.cursor:QTextCursor=self.textCursor()

        self.word_format=QTextCharFormat()
        self.word_format.setForeground(QColor("black"))
        self.word_format.setBackground(QColor("yellow"))

        # Set up the signal for cursor position changes
        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

        self.columnNumberArea= self.ColumnNumberArea(self)

        viewportWidth=self.columnNumberArea.getWidth()

        self.viewport().setFixedWidth(viewportWidth)
        self.viewport().setMaximumWidth(viewportWidth)
        self.setViewportMargins(0,self.columnNumberArea.getHeight(),0,0)
        self.document().setDocumentMargin(0)
        self.viewport().resize(viewportWidth,self.viewport().height())
        self.setFixedWidth(viewportWidth+2*self.fontMetrics().averageCharWidth())

        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.setLineWrapMode(QTextEdit.WidgetWidth)

        
    
    def getLineCount(self):
        return (self.document().characterCount()-1)//(self.columnNumberArea.characterCount())+1
    

    def selectWord(self)->QTextCursor:
        cursor=self.textCursor()
        cursor.movePosition(QTextCursor.Left,QTextCursor.KeepAnchor,1)
        return cursor
    
    def selectByte(self,n:int)->QTextCursor:
        cursor=self.textCursor()
        cursor.setPosition(n)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
        return cursor
    
    def highlightCursor(self,cursor:QTextCursor):
        self.cursor.setCharFormat(QTextCharFormat())
        self.cursor=cursor
        #print(cursor.selection())
        self.cursor.setCharFormat(self.word_format)

    def highlightByte(self,n:int):
        self.highlightCursor(self.selectByte(n))

    def highlightWord(self):
        self.highlightCursor(self.selectWord())

    def onCursorPositionChanged(self):
        self.highlightWord()
    
    def mousePressEvent(self, event:QMouseEvent):
        cursor = self.cursorForPosition(event.pos())
        cursor.clearSelection()
        self.setTextCursor(cursor)


    def keyPressEvent(self, event:QKeyEvent):
        super().keyPressEvent(event)


    def setBytes(self,b:bytes):
        pass

        
        
