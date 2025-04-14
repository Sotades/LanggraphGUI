from sotades.langgraph.i_langgraph import ILanggraph
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
import os

class HitlLanggraph(ILanggraph):

    def __init__(self):
        self.dotenv_loaded = False
        self.system_message = None

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
        pass

    def execute(self):
        pass






