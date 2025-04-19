from abc import ABCMeta, abstractmethod

from langgraph.graph import StateGraph

from sotades.langgraph.state import State


class ILanggraph(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'build_graph') and
                callable(subclass.build_graph) and
                hasattr(subclass, 'execute') and
                callable(subclass.execute_graph) or
                NotImplemented)

    @abstractmethod
    def build_graph(self):
        """Build the Langgraph graph."""
        raise NotImplementedError

    @abstractmethod
    def execute_graph(self, state: State):
        """Execute the Langgraph graph."""
        raise NotImplementedError

    @abstractmethod
    def load_dotenv(self):
        """Load the environment variables"""
        raise NotImplementedError

    @abstractmethod
    def load_system_message(self):
        """Load the system message from a file"""
        raise NotImplementedError

    @abstractmethod
    def setup_initial_state(self):
        """Set up the initial state"""
        raise NotImplementedError

    @abstractmethod
    def display_graph(self):
        """Display the Langgraph graph"""
        raise NotImplementedError
