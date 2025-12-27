from src.utils.rag_utils import retriever_tool
from src.prompts import EMAIL_WRITER_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

from src.state import Email

load_dotenv()


def _create_email_writer_chain(use_rag: bool = False, use_structured_output: bool = False):
    """Create an email writer chain with configurable RAG and structured output"""
    # Create the LLM
    llm = ChatOpenAI(model="gpt-4.1")
    
    # Add RAG tools if needed
    if use_rag:
        llm = llm.bind_tools([retriever_tool])

    # Create the prompt template
    email_writer_prompt = PromptTemplate(
        template=EMAIL_WRITER_PROMPT,
        input_variables=["email_category", "email_content", "context"]
    )
    email_writer_chain = email_writer_prompt | llm
    # Create the chain with optional structured output
    if use_structured_output:
        email_writer_chain = email_writer_prompt | llm.with_structured_output(Email)

    return email_writer_chain


def query_or_email():
    """Create an email writer agent with RAG capabilities and raw output"""
    return _create_email_writer_chain(use_rag=True, use_structured_output=False)

def write_email_with_context():
    """Create an email writer agent with structured output (no RAG but context)"""
    return _create_email_writer_chain(use_rag=False, use_structured_output=True)