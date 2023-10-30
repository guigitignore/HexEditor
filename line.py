from __future__ import annotations
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit,QWidget
from PySide6.QtGui import QPainter,QKeyEvent,QResizeEvent,QTextCursor,QTextCharFormat,QColor,QCursor
from PySide6.QtCore import QSize,Qt,QPoint,Slot,QRect



class ColumnNumberArea(QWidget):
    def __init__(self, editor:CustomTextEdit):
        QWidget.__init__(self, editor)
        self.editor:CustomTextEdit = editor
        self._text=" ".join([format(i,"02X") for i in range(16)])+" "
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
    def __init__(self, editor:CustomTextEdit):
        QWidget.__init__(self, editor)
        self.editor:CustomTextEdit = editor
        self.top=0

    def sizeHint(self):
        return QSize(self.getWidth(), self.getHeight())
    
    def charNeeded(self):
        return len(format((self.editor.getLineCount()-1)<<4,"X"))
    
    def getWidth(self):
        return self.fontMetrics().horizontalAdvance('A') * self.charNeeded()
    
    def getHeight(self):
        return self.editor.viewport().height()
    
    def scroll(self,dx,dy):
        self.top-=dy
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        stepY=self.editor.fontMetrics().lineSpacing()
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
            top+=stepY+1
            topLine+=1

        painter.end()

class CustomTextEdit(QTextEdit):
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

        self.column_number_area= ColumnNumberArea(self)
        self.line_number_area = LineNumberArea(self)

        self.viewport().setFixedWidth(self.columnNumberArea().getWidth())
        self.document().setDocumentMargin(0)
        self.viewport().setMaximumWidth(self.columnNumberArea().getWidth())
        
        self.setLineWrapMode(QTextEdit.WidgetWidth)

        self.lineNumberArea().move(0,self.contentsMargins().top()+self.columnNumberArea().getHeight())
        self.lastLineCount=self.getLineCount()
        
        self.lineNumberUpdate()

        
    def lineNumberArea(self):
        return self.line_number_area

    def columnNumberArea(self):
        return self.column_number_area
    
    def getLineCount(self):
        return (self.document().characterCount()-1)//(self.columnNumberArea().characterCount())+1
    
    def resizeEvent(self, e: QResizeEvent) -> None:
        self.lineNumberArea().resize(self.lineNumberArea().width(),self.viewport().height())
        return super().resizeEvent(e)

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        self.lineNumberArea().scroll(0,dy)
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


    def keyPressEvent(self, event:QKeyEvent):
        #print(self.textCursor().positionInBlock())
        key=event.text().capitalize()

        if event.key()==Qt.Key_Insert:
            position=self.textCursor().position()
            cursor=self.textCursor()
            cursor.movePosition(QTextCursor.Right,QTextCursor.MoveAnchor,3-position%3)
            cursor.insertText("00 ")

        if event.key()==Qt.Key_Delete:
            cursor=self.selectWord()
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1) # select space
            cursor.removeSelectedText()
        

        if key in "0123456789ABCDEF":
            offset=self.textCursor().position()%3
            if offset!=2:
                cursor=self.textCursor()
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                cursor.insertText(key)

            if offset!=1:
                self.moveCursor(QTextCursor.Right,QTextCursor.MoveAnchor)

        if event.key() == Qt.Key_Backspace:
            offset=self.textCursor().position()%3
            if offset:
                cursor=self.textCursor()
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                cursor.removeSelectedText()
                cursor.insertText("0")
                if (offset==1):
                    self.moveCursor(QTextCursor.Left,QTextCursor.MoveAnchor)

            self.moveCursor(QTextCursor.Left,QTextCursor.MoveAnchor)

        if event.key()==Qt.Key_Space:
            self.moveCursor(QTextCursor.Right,QTextCursor.MoveAnchor)
            
        if event.key() in [Qt.Key_Left,Qt.Key_Right,Qt.Key_Up,Qt.Key_Down]:
            super().keyPressEvent(event)


    def lineNumberUpdate(self):
        
        viewportLeftMargin=self.lineNumberArea().getWidth()

        if (viewportLeftMargin!=self.lineNumberArea().width()):
            self.setViewportMargins(viewportLeftMargin,self.columnNumberArea().getHeight(),0,0)
            self.columnNumberArea().move(self.contentsMargins().left()+viewportLeftMargin,0)
            self.lineNumberArea().resize(viewportLeftMargin,self.lineNumberArea().getHeight())
        else:
            self.lineNumberArea().update()

    @Slot()
    def update_line_number_area(self, rect, dy):
        #print("update_line_number_area")
        if dy:
            self.line_number_area.scroll(0, dy)
        
        

class CustomSingleLineEditEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the custom text edit widget
        self.text_edit = CustomTextEdit()

        # Set the QTextEdit as the central widget
        self.setCentralWidget(self.text_edit)

        # Set the main window properties
        self.setWindowTitle("Single Line Text Editor")
        self.setGeometry(100, 100, 600, 100)

# Create the application instance
app = QApplication([])

# Create an instance of the custom QMainWindow
main_window = CustomSingleLineEditEditor()

# Show the main window
main_window.show()

# Run the application event loop
app.exec()
