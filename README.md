<!-- GitHub RAG Application
A modular, production-ready Retrieval-Augmented Generation (RAG) system that takes a GitHub repository as input, extracts and embeds its code, stores embeddings in ChromaDB, and provides a Streamlit-based chat interface powered by GPT-4o mini and orchestrated with LangGraph agent workflows.

Table of Contents
Overview

Features

Architecture

Installation

Configuration

Usage

Project Structure

Contributing

License

Overview
This project enables users to interactively query any public GitHub repository using a Retrieval-Augmented Generation pipeline. It crawls the repository, chunks and embeds the code, stores embeddings in ChromaDB, and provides a chat interface for codebase Q&A using GPT-4o mini. The workflow is managed by LangGraph, ensuring robust, multi-step agentic processing.

Features
GitHub Repository Crawler: Extracts all code files from any public GitHub repository.

Code Chunking: Splits code into manageable, token-limited chunks for efficient embedding and retrieval.

OpenAI Embeddings: Generates vector embeddings for code using OpenAI’s latest models.

ChromaDB Vector Store: Stores and retrieves code embeddings for fast, semantic search.

Streamlit UI: User-friendly interface for repository input and chat-based code exploration.

LangGraph Agent Workflow: Modular, agentic pipeline for validation, processing, and chat.

Supports GPT-4o mini: Leverages state-of-the-art LLM for accurate, context-aware answers.

Architecture
Streamlit Frontend: Collects GitHub repo URL, displays progress, and provides a chat interface.

LangGraph Agent: Orchestrates the workflow: URL validation → repo crawling → chunking → embedding → storage → chat.

ChromaDB: Stores code embeddings and supports similarity search for RAG.

OpenAI API: Generates embeddings and answers user queries with GPT-4o mini.

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/rag_github_app.git
cd rag_github_app
Install dependencies:

bash
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root with the following:

text
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token  # Optional, for higher rate limits
CHROMA_DB_DIR=./chroma_db
Configuration
OpenAI API Key: Required for embeddings and chat.

GitHub Token: Optional but recommended for higher API rate limits.

ChromaDB Directory: Path for persistent vector storage.

Usage
Start the Streamlit app:

bash
streamlit run app/main.py
Workflow:

Enter a GitHub repository URL in the input field.

The app validates the URL, crawls the repo, chunks and embeds code, and indexes it in ChromaDB.

Once processing is complete, use the chat interface to ask questions about the codebase.

The system retrieves relevant code chunks and generates answers using GPT-4o mini.

Project Structure
text
rag_github_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py            # Streamlit UI
│   ├── settings.py        # .env and config
│   ├── repo_crawler.py    # GitHub crawling
│   ├── chunker.py         # Code chunking
│   ├── embedder.py        # Embedding logic
│   ├── vector_store.py    # ChromaDB interface
│   ├── agent.py           # LangGraph agent
│   └── utils.py           # Helpers
│
├── tests/
│   ├── __init__.py
│   └── test_app.py
│
├── requirements.txt
├── .env
├── README.md
└── LICENSE
Each module is isolated for clarity and extensibility.

Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, improvements, or new features. Ensure your code is well-documented and tested.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Inspired by best practices in RAG, LangGraph, and Streamlit agentic workflows.

See related projects and guides for further reading.
 -->


# GitHub RAG Chatbot

A production-ready, conversational Retrieval-Augmented Generation (RAG) system that transforms any GitHub repository into an intelligent chatbot. Built with LangGraph workflows, ChromaDB vector storage, and GPT-4o mini for natural conversations about codebases.

## 🚀 Features

### Core Capabilities
- **Intelligent Repository Processing**: Automatically crawls, analyzes, and indexes any public GitHub repository
- **Conversational Interface**: Persistent chat sessions with full conversation history and context awareness
- **Smart Code Retrieval**: Semantic search through code using vector embeddings for accurate context
- **Real-time Processing**: Live status updates and error handling during repository processing
- **Multi-turn Conversations**: Ask follow-up questions with maintained conversation context

### Technical Features
- **LangGraph Agent Orchestration**: Robust, multi-step agentic workflows with conditional routing
- **ChromaDB Vector Storage**: High-performance vector database for semantic code search
- **OpenAI Integration**: Latest embedding models and GPT-4o mini for intelligent responses
- **Streamlit UI**: Professional, responsive interface with sidebar management and real-time updates
- **Error Recovery**: Comprehensive error handling with user-friendly messages and retry options

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Streamlit UI  │───▶│  LangGraph Agent │───▶│    ChromaDB Store   │
│                 │    │                  │    │                     │
│ • Repository    │    │ • URL Validation │    │ • Vector Embeddings │
│   Management    │    │ • Code Processing│    │ • Semantic Search   │
│ • Chat Interface│    │ • Chat Handling  │    │ • Persistent Storage│
│ • Status Updates│    │ • Error Recovery │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                        │                         │
         └────────────────────────┼─────────────────────────┘
                                  ▼
                        ┌──────────────────┐
                        │   OpenAI API     │
                        │                  │
                        │ • Code Embeddings│
                        │ • GPT-4o Mini    │
                        │ • Context-Aware  │
                        │   Responses      │
                        └──────────────────┘
```

### Workflow Components

1. **Streamlit Frontend**: Modern UI with sidebar controls, real-time status, and persistent chat
2. **LangGraph Agent**: Orchestrates validation → processing → chat with smart routing
3. **ChromaDB Vector Store**: Stores and retrieves code embeddings for semantic search
4. **OpenAI Integration**: Generates embeddings and provides intelligent, context-aware responses

## 📦 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- GitHub token (optional, for higher rate limits)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/rag_github_app.git
   cd rag_github_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_TOKEN=your_github_token_here  # Optional but recommended
   CHROMA_DB_DIR=./chroma_db
   ```

4. **Launch the application**:
   ```bash
   streamlit run app/main.py
   ```

## 🎯 Usage Guide

### Getting Started

1. **Access the Interface**: Open your browser to the Streamlit URL (typically `http://localhost:8501`)
2. **Enter Repository URL**: Paste any public GitHub repository URL in the sidebar
3. **Process Repository**: Click "🚀 Process Repository" and wait for completion
4. **Start Chatting**: Once processed, ask questions about the codebase in the chat interface

### Example Conversations

**Initial Questions:**
- "What does this repository do?"
- "How is the code organized?"
- "What are the main components?"

**Follow-up Questions:**
- "How does the authentication work?"
- "Show me the API endpoints"
- "What testing frameworks are used?"

**Technical Deep-dives:**
- "Explain the database schema"
- "How is error handling implemented?"
- "What are the performance considerations?"

### Advanced Features

- **Repository Switching**: Use "🔄 Process New Repository" to analyze different repos
- **Conversation History**: Full chat history is maintained throughout your session
- **Context Awareness**: Follow-up questions understand previous conversation context
- **Smart Retrieval**: System finds the most relevant code chunks for each query

## 📁 Project Structure

```
rag_github_app/
├── app/
│   ├── main.py              # Enhanced Streamlit UI with chat persistence
│   ├── agent.py             # Extended LangGraph workflows with chat routing
│   ├── settings.py          # Configuration and environment management
│   ├── repo_crawler.py      # GitHub repository crawling and file extraction
│   ├── chunker.py           # Intelligent code chunking strategies
│   ├── embedder.py          # OpenAI embedding generation
│   ├── vector_store.py      # ChromaDB interface and management
├── tests/
│   ├── __init__.py
│   └── test_app.py          # Comprehensive test suite
├── chroma_db/               # ChromaDB persistent storage (auto-created)
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── README.md               # This file
└── LICENSE                 # MIT License
```

<!-- ### Key Improvements in This Version

#### Enhanced `agent.py`:
- **Conversational State Management**: Maintains chat history across multiple queries
- **Smart Routing**: Conditional workflows for new repositories vs. chat-only modes
- **Error Recovery**: Comprehensive error handling with meaningful user feedback
- **Context-Aware Responses**: Previous conversation history informs new responses

#### Improved `main.py`:
- **Professional UI**: Modern interface with custom CSS and responsive design
- **Persistent Sessions**: Chat history and repository state maintained across interactions
- **Real-time Updates**: Live processing status and error notifications
- **Repository Management**: Easy switching between different repositories -->

## ⚙️ Configuration Options

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for embeddings and chat | - |
| `GITHUB_TOKEN` | No | GitHub personal access token for higher rate limits | - |
| `CHROMA_DB_DIR` | No | Directory for ChromaDB persistent storage | `./chroma_db` |

### Advanced Configuration

- **Embedding Model**: Configurable in `embedder.py` (currently using OpenAI's latest)
- **Chunk Size**: Adjustable in `chunker.py` for optimal performance
- **Retrieval Count**: Number of similar chunks retrieved (default: 5)
- **Context Window**: Conversation history length (default: last 3 exchanges)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Install development dependencies: `pip install -r requirements.txt`
4. Run tests: `python -m pytest tests/`

### Contribution Guidelines

- **Code Quality**: Follow PEP 8 style guidelines
- **Documentation**: Update docstrings and README for new features
- **Testing**: Add tests for new functionality
- **Issues**: Use GitHub issues for bug reports and feature requests

### Areas for Contribution

- **Additional Code Languages**: Expand language-specific chunking strategies
- **Advanced RAG Techniques**: Implement hybrid search, reranking, or query expansion
- **UI Enhancements**: Add visualization of code structure or embedding clusters
- **Performance Optimization**: Improve processing speed and memory usage

## 🔧 Troubleshooting

### Common Issues

**Repository Processing Fails**:
- Verify the GitHub URL is correct and the repository is public
- Check your internet connection and GitHub API rate limits
- Ensure OpenAI API key is valid and has sufficient credits

**Chat Not Working**:
- Confirm the repository was processed successfully
- Check OpenAI API key permissions and rate limits
- Verify ChromaDB directory is writable

**Performance Issues**:
- Large repositories may take several minutes to process
- Consider using a GitHub token to avoid rate limiting
- Ensure sufficient disk space for ChromaDB storage

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## 🙏 Acknowledgments

- **LangGraph**: For providing robust agent workflow orchestration
- **ChromaDB**: For efficient vector storage and retrieval
- **Streamlit**: For enabling rapid UI development
- **OpenAI**: For state-of-the-art embeddings and language models

## 🔗 Related Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Ready to chat with any codebase? Get started by processing your first repository!** 🚀