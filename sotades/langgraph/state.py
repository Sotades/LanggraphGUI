from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages, MessagesState


class State(MessagesState):
    input_xsd: Annotated[str, "The XSD of the input to the mapping"]
    output_xsd: Annotated[str, "The XSD of the output from the mapping"]
    xslt: Annotated[str, "The XSLT of the mapping"]