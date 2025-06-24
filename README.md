# Github Repo Chatbot

A conversational Retrieval-Augmented Generation (RAG) system that transforms any GitHub repository into an intelligent chatbot. Built with LangGraph workflows, ChromaDB vector storage, and GPT-4o mini for natural conversations about codebases.

## 🚀 Features

### Core Capabilities
- **Intelligent Repository Processing**: Automatically crawls, analyzes, and indexes any public GitHub repository
- **Conversational Interface**: Persistent chat sessions with full conversation history and context awareness
- **Code Retrieval**: Semantic search through code using vector embeddings for accurate context
- **Real-time Processing**: Live status updates and error handling during repository processing
- **Multi-turn Conversations**: Ask follow-up questions with maintained conversation context

### Technical Features
- **LangGraph Agent Orchestration**: Robust, multi-step agentic workflows with conditional routing
- **ChromaDB Vector Storage**: High-performance vector database for semantic code search
- **OpenAI Integration**: Latest embedding models and GPT-4o mini for intelligent responses
- **Streamlit UI**: Responsive interface with sidebar management and real-time updates
- **Error Recovery**: Comprehensive error handling with user-friendly messages and retry options

## 🏗️ Workflow

![Workflow Diagram](https://github.com/BenLus/Github_Repo_Chatbot/assets/170586907/8a123456-7890-1234-5678-90abcdef1234)


## 🔧 How It Works

### RAG Pipeline Architecture

This system implements a multi-stage RAG pipeline optimized for code understanding and retrieval. The architecture follows modern agentic workflow patterns with state management and conditional routing.

#### 1. **Repository Ingestion**
- URL validation with regex pattern matching for GitHub repository extraction
- GitHub API integration with tree endpoint for comprehensive file discovery

#### 2. **Content Preprocessing**
- Token-aware chunking using OpenAI's `o200k_base` tokenizer for GPT-4o mini compatibility
- Sliding window approach with configurable overlap to preserve semantic continuity
- Metadata preservation including file paths, line ranges, and repository context

#### 3. **Vector Embedding Pipeline**
- Batch processing through OpenAI's `text-embedding-3-small` model (1536-dimensional vectors)
- Optimized API utilization with configurable batch sizes for cost efficiency
- Semantic encoding of code semantics, syntax patterns, and contextual relationships

#### 4. **Vector Storage & Indexing**
- ChromaDB integration with persistent storage for production scalability
- Sanitized collection naming with deterministic ID generation for deduplication
- Similarity search capabilities using cosine distance for semantic retrieval

#### 5. **Conversational RAG Interface**
- Query embedding generation with identical model consistency for retrieval accuracy
- Top-k similarity search with configurable retrieval parameters
- Context assembly combining retrieved chunks with conversation history for multi-turn coherence
- GPT-4o mini inference with carefully engineered prompts for code-specific responses

## 📦 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- GitHub token (optional, for higher rate limits)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BenLus/Github_Repo_Chatbot.git
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

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## 🔗 Related Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Ready to chat with any codebase? Get started by processing your first repository!** 🚀