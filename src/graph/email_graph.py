from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from src.utils.rag_utils import get_retriever_tool
from src.nodes import NODES
from src.state import GraphState
import os

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

class EmailSupportGraph():

    def __init__(self):
        workflow = StateGraph(GraphState)
        workflow.add_node("load_email", NODES["email_listener"])
        workflow.add_node("categorize_email", NODES["email_categorizer"])
        workflow.add_node("query_or_email", NODES["query_or_email"])
        workflow.add_node("retrieve", ToolNode([get_retriever_tool()]))
        workflow.add_node("write_email_with_context", NODES["write_email_with_context"])

        workflow.add_edge(START, "load_email")
        workflow.add_edge("load_email", "categorize_email")
        workflow.add_edge("categorize_email", "query_or_email")

        workflow.add_conditional_edges(
            "query_or_email",
            tools_condition,
            {
                "tools": "retrieve",
                END: "write_email_with_context"
            }
        )

        workflow.add_edge("retrieve", "write_email_with_contex")
        workflow.add_edge("write_email_with_context", END)

        self.graph = workflow.compile()

emailSupportGraph = EmailSupportGraph().graph

