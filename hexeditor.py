from __future__ import annotations
from PySide6.QtWidgets import QTextEdit,QWidget,QScrollBar
from PySide6.QtGui import QPainter,QKeyEvent,QResizeEvent,QTextCursor,QTextCharFormat,QColor,QMouseEvent
from PySide6.QtCore import QSize,Qt,Slot,Signal


class HexEditor(QTextEdit):

    class ColumnNumberArea(QWidget):
        def __init__(self, editor:HexEditor):
            QWidget.__init__(self, editor)
            self.editor:HexEditor = editor
            self._text=" ".join([format(i,"02X") for i in range(16)])+' '
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
    

    class LineNumberArea(QWidget):
        def __init__(self, editor:HexEditor):
            QWidget.__init__(self, editor)
            self.editor:HexEditor = editor
            self.top=0

        def sizeHint(self):
            return QSize(self.getWidth(), self.getHeight())
        
        def charNeeded(self):
            return len(format((self.editor.getLineCount()-1)<<4,"X"))
        
        def getWidth(self):
            return self.fontMetrics().horizontalAdvance('A') * self.charNeeded()+2
        
        def getHeight(self):
            return self.editor.viewport().height()
        
        def scroll(self,dx,dy):
            self.top-=dy
            self.update()
        
        def paintEvent(self, event):
            painter = QPainter(self)
            stepY=self.editor.fontMetrics().lineSpacing()+1
            top=event.rect().topLeft().y()
            topLine=(self.top+top)//stepY

            offset=(self.top+top)%stepY
            if offset:
                top-=offset
                top+=stepY
                topLine+=1
            
            painter.fillRect(event.rect(), Qt.red)

            
            bottom=event.rect().bottomLeft().y()
            totalLine=self.editor.getLineCount()

            hexformat="0{}X".format(self.charNeeded())

            while (top<bottom):
                if (topLine>=totalLine):
                    break
                painter.drawText(0, top, self.width(), self.height(), Qt.AlignLeft, format(topLine<<4,hexformat))
                top+=stepY
                topLine+=1

            painter.end()

    class VerticalScrollbar(QScrollBar):
        def __init__(self,editor:HexEditor):
            super().__init__(editor)
            



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
        self.lineNumberArea = self.LineNumberArea(self)
        self.verticalSrollbar=QScrollBar(Qt.Vertical,self)
        self.verticalSrollbar.setFixedWidth(self.fontMetrics().averageCharWidth()*2)
        self.verticalSrollbar.valueChanged.connect(self.verticalScrollBar().setValue)

        viewportWidth=self.columnNumberArea.getWidth()

        self.viewport().setFixedWidth(viewportWidth)
        #self.viewport().setMaximumWidth(viewportWidth)
        self.document().setDocumentMargin(0)
        self.viewport().resize(viewportWidth,self.viewport().height())

        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setLineWrapMode(QTextEdit.WidgetWidth)

        self.lineNumberArea.move(0,self.contentsMargins().top()+self.columnNumberArea.getHeight())

        self.lastLineCount=self.getLineCount()
        
        self.lineNumberUpdate()

    
    def getLineCount(self):
        return (self.document().characterCount()-1)//(self.columnNumberArea.characterCount())+1
    
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.lineNumberArea.resize(self.lineNumberArea.width(),self.viewport().height())
        self.verticalSrollbar.setRange(0, self.verticalScrollBar().maximum())
        
        self.verticalSrollbar.setFixedHeight(self.viewport().height())
        

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        self.lineNumberArea.scroll(0,dy)
        return super().scrollContentsBy(dx, dy)
    

    def selectWord(self)->QTextCursor:
        cursor=self.textCursor()
        cursor.movePosition(QTextCursor.Left,QTextCursor.MoveAnchor,cursor.position()%3)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 2)
        return cursor
    
    def selectByte(self,n:int)->QTextCursor:
        cursor=self.textCursor()
        cursor.setPosition(n*3)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 2)
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
        #print(self.document().characterCount()-1,self.columnNumberArea().characterCount())
        currentLineCount=self.getLineCount()
        if (self.lastLineCount!=currentLineCount):
            self.lineNumberUpdate()
            self.lastLineCount=currentLineCount

        self.highlightWord()
    
    def mousePressEvent(self, event:QMouseEvent):
        cursor = self.cursorForPosition(event.pos())
        cursor.clearSelection()
        self.setTextCursor(cursor)


    def keyPressEvent(self, event:QKeyEvent):
        #print(self.textCursor().positionInBlock())
        key=event.text().capitalize()
        
        if event.key() in [Qt.Key_Left,Qt.Key_Right,Qt.Key_Up,Qt.Key_Down]:
            super().keyPressEvent(event)

        elif event.key()==Qt.Key_Insert:
            position=self.textCursor().position()
            cursor=self.textCursor()
            cursor.movePosition(QTextCursor.Right,QTextCursor.MoveAnchor,3-position%3)
            cursor.insertText("00 ")

        elif event.key()==Qt.Key_Delete:
            cursor=self.selectWord()
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1) # select space
            cursor.removeSelectedText()
        

        elif key in "0123456789ABCDEF" and not self.textCursor().atEnd():
            offset=self.textCursor().position()%3
            if offset!=2:
                cursor=self.textCursor()
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                cursor.insertText(key)

            if offset!=0:
                self.moveCursor(QTextCursor.Right,QTextCursor.MoveAnchor)

        elif event.key() == Qt.Key_Backspace:
            offset=self.textCursor().position()%3
            if offset:
                cursor=self.textCursor()
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                cursor.removeSelectedText()
                cursor.insertText("0")
                if (offset==1):
                    self.moveCursor(QTextCursor.Left,QTextCursor.MoveAnchor)

            self.moveCursor(QTextCursor.Left,QTextCursor.MoveAnchor)

        elif event.key()==Qt.Key_Space:
            self.moveCursor(QTextCursor.Right,QTextCursor.MoveAnchor)


    def lineNumberUpdate(self):
        
        viewportLeftMargin=self.lineNumberArea.getWidth()

        if (viewportLeftMargin!=self.lineNumberArea.width()):
            viewportTopMargin=self.columnNumberArea.getHeight()

            self.setViewportMargins(viewportLeftMargin,viewportTopMargin,0,0)
            self.columnNumberArea.move(self.contentsMargins().left()+viewportLeftMargin,0)

            self.verticalSrollbar.move(viewportLeftMargin+self.viewport().width(),viewportTopMargin)

            self.lineNumberArea.resize(viewportLeftMargin,self.lineNumberArea.getHeight())

            self.verticalSrollbar.setRange(0, self.verticalScrollBar().maximum())

            self.setMaximumWidth(viewportLeftMargin+self.columnNumberArea.getWidth()+self.verticalSrollbar.width())
        else:
            self.lineNumberArea.update()

    def setBytes(self,b:bytes):
        self.setText(" ".join([format(byte,'02X') for byte in b]))


    @Slot()
    def update_line_number_area(self, rect, dy):
        #print("update_line_number_area")
        if dy:
            self.line_number_area.scroll(0, dy)
        
        
