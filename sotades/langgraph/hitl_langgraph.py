from IPython.display import Image, display
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from sotades.langgraph.i_langgraph import ILanggraph
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
import os

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph

from sotades.langgraph.state import State


class HitlLanggraph(ILanggraph):

    def setup_initial_state(self):
        # TODO
        self.load_xsd_schemas()
        self.load_system_message()
        pass

    def __init__(self):
        self.graph: CompiledStateGraph = None
        self.dotenv_loaded = False
        self.system_message = None
        self.state: State = None


    def load_dotenv(self):
        self.dotenv_loaded = load_dotenv()

    def load_system_message(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        system_message_path = os.path.join(current_dir, 'system_message.txt')
        
        try:
            with open(system_message_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            self.system_message = SystemMessage(content=content)
            return self.system_message
        except FileNotFoundError:
            raise FileNotFoundError(f"System message file not found at {system_message_path}")

    def build_graph(self):

        # Nodes
        def gui_initial_send(state: State):
            return state

        # Graph
        builder = StateGraph(State)

        # Define nodes
        builder.add_node("gui_initial_send", gui_initial_send)

        # Define edges: these determine the control flow
        builder.add_edge(START, "gui_initial_send")
        builder.add_edge("gui_initial_send", END)

        memory = MemorySaver()

        self.graph = builder.compile(checkpointer=memory)

        return self.graph


    def execute_graph(self, state: State):

        # Thread
        thread = {"configurable": {"thread_id": "1"}}

        # PAY ATTENTION HERE: this runs the graph, but since the graph
        # has a breakpoint configured, it will pause the execution
        # before using a tool.
        for event in self.graph.stream(state, thread, stream_mode="values"):
            event['messages'][-1].pretty_print()
            print(f"Next state: {self.graph.get_state(thread).next}")

    def load_xsd_schemas(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)  # Go up to sotades directory
        xsd_path = os.path.join(parent_dir, 'xml', 'ZTELINVOIC.INVOIC02.ZTELINVOIC02.xsd')
        
        try:
            with open(xsd_path, 'r', encoding='utf-8') as file:
                self.input_xsd = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"XSD schema file not found at {xsd_path}")





