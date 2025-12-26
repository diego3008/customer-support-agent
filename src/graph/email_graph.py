from langgraph.graph import START, END, StateGraph
from src.nodes import NODES
from src.state import GraphState
import os

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class EmailSupportGraph():

    def __init__(self):
        workflow = StateGraph(GraphState)
        workflow.add_node("load_email", NODES["email_listener"])
        workflow.add_node("categorize_email", NODES["email_categorizer"])
        workflow.add_edge(START, "load_email")
        workflow.add_edge("load_email", "categorize_email")
        workflow.add_edge("categorize_email", END)

        self.graph = workflow.compile()

emailSupportGraph = EmailSupportGraph().graph

