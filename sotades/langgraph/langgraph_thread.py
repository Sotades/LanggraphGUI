import asyncio
import time

from PySide6 import QtAsyncio
from PySide6.QtCore import Signal
from PySide6.QtAsyncio import QAsyncioEventLoop
from PySide6.QtCore import QThread


class LangGraphThread(QThread):

    # Define a custom signal from within this class. It should be available to all other
    # classes that inherit from QObject.
    langgraph_signal = Signal(str)

    def __init__(self, loop: QAsyncioEventLoop):
        super().__init__()

        # Pass the Event Loop in so we can access it from this thread.
        # Then we can use asyncio queues and pass data between the Langgraph thread
        # and the main program thread.
        self.loop = loop

        # Define a Future to await.
        self.future = asyncio.Future()

    async def emit_signal_and_wait(self):
        # Emit signal from langgraph thread. Can we process it in the main thread?
        self.langgraph_signal.emit("Message from langgraph thread")
        print("Emitted signal from langgraph thread")
        print("Awaiting future to continue processing")
        await self.future
        print("Received future")


    def run(self):
        QtAsyncio.run(self.emit_signal_and_wait())
        while(True):
            time.sleep(2)
            print("Awaiting future to stop")

        print("Thread complete")
