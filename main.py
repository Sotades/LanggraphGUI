from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt

import PySide6.QtAsyncio as QtAsyncio

import asyncio
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Langgraph HITL Demo")
        button = QPushButton("Start Langchain")
        button.clicked.connect(lambda: asyncio.create_task(self.langchain_app()))
        # Set the central widget of the Window.
        self.setCentralWidget(button)

    async def langchain_app(self):
            await asyncio.sleep(1)
            print("End langchain_app")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)