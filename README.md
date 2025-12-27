# Customer Support Agent

An intelligent AI-powered customer support system built with LangGraph that automatically processes incoming emails, categorizes them, retrieves relevant information, and generates appropriate responses.

## Overview

This project implements an automated customer support workflow that integrates with Gmail to process incoming emails. It uses AI agents to categorize emails, retrieve relevant information from a knowledge base, and generate professional responses to customers.

## Frameworks and Technologies

- **LangGraph**: Core workflow orchestration framework for building stateful, cyclic AI agents
- **LangChain**: Foundation framework for building AI applications with LLMs
- **Google Gmail API**: Integration with Gmail for email processing
- **ChromaDB**: Vector database for retrieval-augmented generation (RAG)
- **Pydantic**: Data validation and serialization
- **AWS/OpenAI**: LLM provider integrations

## Project Structure

```
customer-support-agent/
├── main.py                  # Entry point for the application
├── requirements.txt         # Python dependencies
├── src/                     # Main source code directory
│   ├── agents/             # AI agents for specific tasks
│   │   ├── email_categorizer.py
│   │   └── email_writer.py
│   ├── graph/              # Workflow graph definition
│   │   └── email_graph.py
│   ├── nodes/              # Graph nodes implementing workflow steps
│   │   ├── email_categorizer.py
│   │   ├── email_listener.py
│   │   ├── email_sender.py
│   │   └── email_writer.py
│   ├── prompts/            # AI prompt templates
│   ├── state.py            # State definitions for the workflow
│   └── utils/              # Utility functions
│       ├── gmail_utils.py
│       └── rag_utils.py
├── chroma_db/              # Chroma vector database storage
└── credentials.json        # Gmail API credentials
```

## Workflow Architecture

The system follows a structured workflow orchestrated by LangGraph:

1. **Email Listening**: Monitors Gmail for new incoming emails
2. **Email Categorization**: AI agent categorizes emails (product enquiry, customer complaint, feedback, unrelated)
3. **Conditional Processing**: 
   - For product inquiries and complaints: Retrieves relevant information from knowledge base
   - For other categories: Proceeds directly to response generation
4. **Response Generation**: AI agent crafts a professional, context-aware response
5. **Email Sending**: Automatically sends the response back to the customer

## Key Components

### AI Agents
- **Email Categorizer**: Specialized agent that accurately identifies the intent behind customer emails
- **Email Writer**: Context-aware agent that generates professional responses based on email content and retrieved information

### Graph Workflow
The LangGraph-based workflow ensures stateful processing with the ability to:
- Maintain conversation context
- Handle complex branching logic
- Provide observability and debugging capabilities

### RAG Integration
Retrieval-Augmented Generation capabilities allow the system to:
- Access up-to-date company knowledge
- Provide accurate information in responses
- Reduce hallucinations in generated content

## Setup and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure Gmail API credentials in `credentials.json`

3. Run the application:
   ```bash
   python main.py
   ```

## Features

- **Automated Email Processing**: Automatically detects, categorizes, and responds to incoming emails
- **Intelligent Categorization**: Accurately classifies emails into appropriate support categories
- **Context-Aware Responses**: Generates responses based on both email content and relevant knowledge base information
- **Extensible Architecture**: Modular design allows easy addition of new features and capabilities
- **Professional Communication**: Maintains consistent, professional tone in all customer interactions

This system significantly reduces manual effort in customer support while ensuring consistent, accurate, and timely responses to customer inquiries.
