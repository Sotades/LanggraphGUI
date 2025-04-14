from abc import ABCMeta, abstractmethod


class ILanggraph(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'build_graph') and
                callable(subclass.build_graph) and
                hasattr(subclass, 'execute') and
                callable(subclass.execute) or
                NotImplemented)

    @abstractmethod
    def build_graph(self):
        """Build the Langgraph graph."""
        raise NotImplementedError

    @abstractmethod
    def execute(self):
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