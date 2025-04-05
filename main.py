from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Langgraph HITL Demo")
        button = QPushButton("Start Langchain")
        button.clicked.connect(self.start_langchain_app)
        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def start_langchain_app(self):
        print("Starting Langchain Demo")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()