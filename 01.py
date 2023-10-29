import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setStatusBar(QStatusBar(self))
        self.status = self.statusBar()
        self.status.addPermanentWidget(QLabel("(c) Carlier"))
        self.status.showMessage("Hello", 3000)

        # Création des boutons
        self.btn_0 = QPushButton("Click 0", self)
        self.btn_1 = QPushButton("Click 1", self)
        self.btn_2 = QPushButton("Click 2", self)

        # Création de la mise en page
        layout = QVBoxLayout()
        layout.addWidget(self.btn_0)
        layout.addWidget(self.btn_1)
        layout.addWidget(self.btn_2)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.btn_0.clicked.connect(self.action_btn_0)

    def action_btn_0(self):
        # le slot...
        self.status.showMessage("Ola !", 300)
        QMessageBox.information(self, "Titre", "Texte")


app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Richnou is great")
window.show()

app.exec()