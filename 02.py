import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # On crée une grille
        layout = QGridLayout()
        central_widget.setLayout(layout)

        btn = QPushButton("Bouton 1")
        layout.addWidget(btn, 0, 0) # ligne 0, colone 0

        layout.addWidget(QLabel("Label"), 1, 0)
        layout.addWidget(QTextEdit(), 2, 0)
        layout.addWidget(QCalendarWidget(), 3, 0)

        lcd_number = QLCDNumber()
        lcd_number.setMinimumHeight(50)
        lcd_number.display(123)
        layout.addWidget(lcd_number, 4, 0)

        # Création d'un QFormLayout
        form_layout = QFormLayout()
        layout.addLayout(form_layout, 0, 1, 5, 1)

        line_edit = QLineEdit()
        line_edit.setText("Richnou")
        form_layout.addRow("Line Edit:", line_edit)
        form_layout.addRow("Text Edit:", QTextEdit())
        form_layout.addRow("Text Edit:", QTextEdit())


        form_layout.addRow("Time:", QTimeEdit())
        form_layout.addRow("Date:", QDateEdit())
        form_layout.addRow("DateTime", QDateTimeEdit())

        form_layout.addRow("", QCheckBox("S'abonner ?"))

        colors = ["Rouge", "Vert", "Jaune", "Bleu"]
        color_group = QButtonGroup(self)
        color_layout = QHBoxLayout()
        for index, color in enumerate(colors):
            r = QRadioButton(color)
            color_group.addButton(r)
            color_layout.addWidget(r)
            if index == 0:
                r.setChecked(True)
        form_layout.addRow("liste", color_layout)

        combo = QComboBox()
        combo.addItem("Chouquette")
        combo.addItem("Croissant")
        combo.addItem("Pain au chocolat")
        combo.addItems(colors)
        combo.setCurrentIndex(0)
        form_layout.addRow("Liste", combo)


app = QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Richnou is great")
window.show()

app.exec()