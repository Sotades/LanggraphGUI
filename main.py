from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt

import PySide6.QtAsyncio as QtAsyncio

import asyncio
import sys
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from typing import Literal

from langgraph.graph import END, StateGraph, START
from langchain_core.messages import HumanMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Queues for exchanging data between langgraph and PyQt widgets
        self.langgraph_to_pyqt_queue = asyncio.Queue()
        self.pyqt_to_langgraph_queue = asyncio.Queue()

        self.setWindowTitle("Langgraph HITL Demo")
        button = QPushButton("Start Langchain")
        button.clicked.connect(lambda: asyncio.create_task(self.langchain_app()))
        # Set the central widget of the Window.
        self.setCentralWidget(button)

    async def langchain_app(self):
            result = load_dotenv()

            @tool
            def search(query: str):
                """Call to surf the web."""
                # This is a placeholder, but don't tell the LLM that...
                return ["The answer to your question lies within."]

            tools = [search]

            tool_node = ToolNode(tools)

            model = ChatOpenAI(model="gpt-4o")

            model = model.bind_tools(tools)

            # Define the function that determines whether to continue or not
            def should_continue(state: State) -> Literal["end", "continue"]:
                messages = state["messages"]
                last_message = messages[-1]
                # If there is no tool call, then we finish
                if not last_message.tool_calls:
                    return "end"
                # Otherwise if there is, we continue
                else:
                    return "continue"

            # Define the function that calls the model
            def call_model(state: State):
                messages = state["messages"]
                response = model.invoke(messages)
                # We return a list, because this will get added to the existing list
                return {"messages": [response]}

            # Define a new graph
            workflow = StateGraph(State)

            # Define the two nodes we will cycle between
            workflow.add_node("agent", call_model)
            workflow.add_node("action", tool_node)

            # Set the entrypoint as `agent`
            # This means that this node is the first one called
            workflow.add_edge(START, "agent")

            # We now add a conditional edge
            workflow.add_conditional_edges(
                # First, we define the start node. We use `agent`.
                # This means these are the edges taken after the `agent` node is called.
                "agent",
                # Next, we pass in the function that will determine which node is called next.
                should_continue,
                # Finally we pass in a mapping.
                # The keys are strings, and the values are other nodes.
                # END is a special node marking that the graph should finish.
                # What will happen is we will call `should_continue`, and then the output of that
                # will be matched against the keys in this mapping.
                # Based on which one it matches, that node will then be called.
                {
                    # If `tools`, then we call the tool node.
                    "continue": "action",
                    # Otherwise we finish.
                    "end": END,
                },
            )

            # We now add a normal edge from `tools` to `agent`.
            # This means that after `tools` is called, `agent` node is called next.
            workflow.add_edge("action", "agent")

            # Finally, we compile it!
            # This compiles it into a LangChain Runnable,
            # meaning you can use it as you would any other runnable
            app = workflow.compile()

            inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}
            messages = app.invoke(inputs)
            await self.langgraph_to_pyqt_queue.put(messages)

            for m in messages['messages']:
                m.pretty_print()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    QtAsyncio.run(handle_sigint=True)