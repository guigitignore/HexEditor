import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from hexeditor import HexEditor
from connector import EditorConnector  
from plaintexteditor import PlainTextEditor      
from document import TextDocument
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setMinimumSize(800, 600)
        self.document=TextDocument()
        # Create a layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Plain text"), 1, 2)
        layout.addWidget(QLabel("Hexa text"), 1, 1)

        self.metadata=QLabel()
        self.metadata.setWordWrap(True)

        self.clear_text = PlainTextEditor(self.document)
        self.hexa_text = HexEditor(self.document)

        self.connector=EditorConnector(self.clear_text,self.hexa_text)


        metadataTitle=QLabel("Metadata")
        metadataTitle.setAlignment(Qt.AlignCenter)
        

        layout.addWidget(self.clear_text, 2, 2)
        layout.addWidget(self.hexa_text, 2, 1)
        layout.addWidget(metadataTitle, 3, 1, 1, 2)
        layout.addWidget(self.metadata, 4, 1, 1, 2)

        #layout.setColumnStretch(1, 1)
        #layout.setColumnStretch(2, 2)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create the "Open" action
        open_action = QAction("Open (Ctrl+O)", self)
        open_action.triggered.connect(self.open_file)

        file_menu.addAction(open_action)

        open_url_action = QAction("Open from URL", self)
        open_url_action.triggered.connect(self.open_file_url)

        file_menu.addAction(open_url_action)

        save_file_action = QAction("Save file (Ctrl+S)", self)
        save_file_action.triggered.connect(self.save_file)

        file_menu.addAction(save_file_action)


        save_metadata_action = QAction("Save metadata to json", self)
        save_metadata_action.triggered.connect(self.save_metadata_file)

        file_menu.addAction(save_metadata_action)

        # Add the "Open" action to the "File" menu
        file_menu.addAction(open_action)

        QShortcut(QKeySequence('Ctrl+O'), self).activated.connect(self.open_file)
        QShortcut(QKeySequence('Ctrl+S'), self).activated.connect(self.save_file)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setWindowTitle("Choose a file to open")
        filename, _ = dialog.getOpenFileName()

        if (filename):
            if self.document.openFile(filename):
                self.hexa_text.updateBytes()
                self.metadata.setText(str(self.document.getMetadata()))
            else:
                self.showErrorPopup("Open file","Fail to open file")

    def open_file_url(self):
        url, ok = QInputDialog.getText(self, 'Enter URL', 'URL:')

        if ok and url:
            if self.document.openURL(url):
                self.hexa_text.updateBytes()
                self.metadata.setText(str(self.document.getMetadata()))
            else:
                self.showErrorPopup("Open from URL","Fail to fetch data")

    def save_file(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)")

        if filePath:
            if self.document.writeFile(filePath):
                self.showInfoPopup("Save file","File successfully written")
            else:
                self.showErrorPopup("Save file","Cannot write the file")

    def save_metadata_file(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File","", "(*.json)")

        if filePath:
            if self.document.writeMetadata(filePath):
                self.showInfoPopup("Save metadata","Metadatada successfully written")
            else:
                self.showErrorPopup("Save metadata","Cannot write the file")

    def showErrorPopup(self,title,message):
        # Create a QMessageBox with a critical icon
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInfoPopup(self,title,message):
        # Create a QMessageBox with a critical icon
        msg = QMessageBox()
        msg.setIcon(QMessageBox.information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
                

                

app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Hex editor")
window.show()

app.exec()
