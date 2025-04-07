import os
import asyncio
import time

from PySide6 import QtAsyncio
from PySide6.QtCore import Signal
from PySide6.QtAsyncio import QAsyncioEventLoop
from PySide6.QtCore import QThread

from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph


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

    # async def emit_signal_and_wait(self):
        # # Emit signal from langgraph thread. Can we process it in the main thread?
        # self.langgraph_signal.emit("Message from langgraph thread")
        # print("Emitted signal from langgraph thread")
        # print("Awaiting future to continue processing")
        # await self.future
        # print("Received future")


    def run(self):
        result = load_dotenv()

        self.chatModel4o = ChatOpenAI(model="gpt-4o")

        # Build graph
        builder = StateGraph(MessagesState)
        builder.add_node("simple_llm", self.simple_llm)

        # Add the logic of the graph
        builder.add_edge(START, "simple_llm")
        builder.add_edge("simple_llm", END)

        # Compile the graph
        graph = builder.compile()

        from pprint import pprint
        from langchain_core.messages import AIMessage, HumanMessage

        messages = graph.invoke({"messages": HumanMessage(content="Where is the Golden Gate Bridge?")})

        for m in messages['messages']:
            m.pretty_print()

        print("Langgraph thread complete")

    # Node
    def simple_llm(self, state: MessagesState):
        return {"messages": [self.chatModel4o.invoke(state["messages"])]}



