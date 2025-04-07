from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QTimer

import PySide6.QtAsyncio as QtAsyncio

import asyncio
import sys

from sotades.langgraph.langgraph_thread import LangGraphThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Langgraph HITL Demo")
        button = QPushButton("Start Langchain")
        button.clicked.connect(self.start_langchain_app)
        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def start_langchain_app(self):
        print("Starting Langchain Code Thread")
        # Create thread and start it.
        loop = asyncio.get_running_loop()
        self.langgraph_thread = LangGraphThread(loop=loop)
        self.langgraph_thread.start()

        # Have to connect the signal to the slot here, because earlier langgraph_thread
        # instance does not exist.
        self.langgraph_thread.langgraph_signal.connect(self.process_langgraph_signal)

    def process_langgraph_signal(self):
        print("Processing Langgraph signal")

        # Single shot timer fires after 10 seconds to simulate the return of a future.
        QTimer.singleShot(5000, self.langgraph_thread.future.set_result("Langgraph signal processed"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)