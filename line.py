from __future__ import annotations
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit,QWidget,QScrollArea
from PySide6.QtGui import QPainter,QWheelEvent
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

    
    def paintEvent(self, event):
        #print(f"paintevent {self.width()}")
        #cursor = self.editor.cursorForPosition(self.editor.viewport().rect().topLeft())
        #print(cursor.position(),self.editor.viewport().rect().topLeft())
        
        painter = QPainter(self)
        print(self.top//self.editor.fontMetrics().height())
        
        painter.fillRect(event.rect(), Qt.red)
        top=event.rect().topLeft().y()
        bottom=event.rect().bottomLeft().y()
        stepY=self.editor.fontMetrics().height()
    

        hexformat="0{}X".format(self.charNeeded())
        textCursor=self.editor.textCursor()

        y=self.editor.cursorRect(textCursor).topLeft().y()
        lineLenght=self.editor.columnNumberArea().characterCount()
        lineNumber=textCursor.position()//lineLenght

        """
        if textCursor.position()%lineLenght==0 and textCursor.position():
            lineNumber-=1
            print("increment")
            pass
        
        

        maxLine=self.editor.getLineCount()

        painter.setPen(Qt.black)
        painter.setFont(self.editor.font())
        
        while (y>=top):
            y-=stepY
            lineNumber-=1

        while (y<=bottom):
            painter.drawText(0, y, self.width(), self.height(), Qt.AlignLeft, format(lineNumber<<4,hexformat))
            y+=stepY
            lineNumber+=1
            if lineNumber>=maxLine:
                break
        """
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

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        self.lineNumberArea().scroll(0,dy)
        return super().scrollContentsBy(dx, dy)

    def onCursorPositionChanged(self):
        #print(self.document().characterCount()-1,self.columnNumberArea().characterCount())
        currentLineCount=self.getLineCount()
        if (self.lastLineCount!=currentLineCount):
            self.lineNumberUpdate()
            self.lastLineCount=currentLineCount

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
