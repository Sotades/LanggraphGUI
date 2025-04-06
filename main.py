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
        button.clicked.connect(self.start_langgraph_app)
        # Set the central widget of the Window.
        self.setCentralWidget(button)

        self.langgraph_app_status = 'Not started'

    def start_langgraph_app(self):
        if self.langgraph_app_status == 'Started':
            print('Already started')
        else:
            self.langgraph_app_status = 'Started'
            print("Starting Langchain Code Thread")

            # Create thread and start it.
            loop = asyncio.get_running_loop()
            self.langgraph_thread = LangGraphThread(loop=loop)
            self.langgraph_thread.start()

    def check_for_langgraph_data(self):
        print("Checking for Langgraph Data")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)