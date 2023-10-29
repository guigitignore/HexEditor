import sys
import time
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(600, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setText("https://www.google.fr/")
        self.send_button = QPushButton("Send Request")

        self.response_label = QLabel("Response:")
        self.response_text = QTextEdit()

        self.info_label = QLabel("Info:")
        self.info_text = QTextEdit()

        self.header_table = QTableWidget()
        self.header_table.setColumnCount(2)
        self.header_table.setHorizontalHeaderLabels(["Header", "Value"])
        self.header_table.setColumnWidth(0, 150)
        self.header_table.setColumnWidth(1, 300)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_label)
        layout.addWidget(self.response_text)
        layout.addWidget(self.info_label)
        layout.addWidget(self.info_text)
        layout.addWidget(self.header_table)

        central_widget.setLayout(layout)

        self.send_button.clicked.connect(self.send_request)

        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_response)

    def handle_response(self, reply):
        elapsed_time = time.time() - self.start_time
        self.send_button.setEnabled(True)
        
        self.info_text.append(f"Response Time: {elapsed_time:.2f} seconds")
        if reply.error() == QNetworkReply.NoError:
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            self.info_text.append(f"HTTP Status Code: {status_code}")

            content = reply.readAll().data().decode("utf-8")
            self.response_text.setPlainText(content)

            headers = reply.rawHeaderList()
            for header in headers:
                header_cell = QTableWidgetItem(header.data().decode("utf-8"))
                value_cell = QTableWidgetItem(reply.rawHeader(header).data().decode("utf-8"))

                self.header_table.insertRow(self.header_table.rowCount())
                self.header_table.setItem(self.header_table.rowCount() - 1, 0, header_cell)
                self.header_table.setItem(self.header_table.rowCount() - 1, 1, value_cell)

        else:
            self.info_text.append("Error: " + reply.errorString())

    def send_request(self):
        url = self.url_input.text()
        if url:
            self.send_button.setEnabled(False)
            self.info_text.clear()
            self.header_table.setRowCount(0)
            self.response_text.clear()
            self.start_time = time.time()

            request = QNetworkRequest(QUrl(url))
            self.network_manager.get(request)

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("HTTP")
window.show()
app.exec()
