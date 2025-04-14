from unittest import TestCase

from langchain_core.messages import SystemMessage

from sotades.langgraph.hitl_langgraph import HitlLanggraph


class TestHitlLanggraph(TestCase):
    def setUp(self):
        self.langgraph = HitlLanggraph()

    def test_build_graph(self):
        self.fail()

    def test_execute(self):
        self.fail()

    def test_load_dotenv(self):
        self.langgraph.load_dotenv()
        self.assertEqual(self.langgraph.dotenv_loaded, True)

    def test_load_system_message(self):
        self.langgraph.load_system_message()
        self.assertIsInstance(self.langgraph.system_message, SystemMessage)

