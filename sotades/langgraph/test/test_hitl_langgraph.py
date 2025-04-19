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

    def test_load_xsd_schemas(self):
        # Call the method
        self.langgraph.load_xsd_schemas()
        
        # Check that input_xsd was loaded
        self.assertIsNotNone(self.langgraph.input_xsd)
        
        # Check that it contains actual XSD content by looking for common XML schema elements
        self.assertIn('<?xml', self.langgraph.input_xsd)
        self.assertIn('xsd:schema', self.langgraph.input_xsd)

