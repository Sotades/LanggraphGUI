import asyncio

from PySide6 import QtAsyncio
from PySide6.QtAsyncio import QAsyncioEventLoop
from PySide6.QtCore import QThread


class LangGraphThread(QThread):

    def __init__(self, loop: QAsyncioEventLoop):
        super().__init__()

        # Pass the Event Loop in so we can access it from this thread.
        # Then we can use asyncio queues and pass data between the Langgraph thread
        # and the main program thread.
        self.loop = loop

    def run(self):

        print("Thread complete")
