"""
agent.py

Defines the LangGraph agent workflow for the RAG application:
1. Validates the GitHub URL.
2. Crawls, chunks, embeds, and stores the repo.
3. Handles chat queries using retrieval-augmented generation.
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import List, Dict, Any
from embedder import EmbeddingGenerator
from vector_store import ChromaDBManager
from openai import OpenAI
from settings import OPENAI_API_KEY, GITHUB_TOKEN, CHROMA_DB_DIR
from repo_crawler import GitHubRepoCrawler
from chunker import CodeChunker
from embedder import EmbeddingGenerator
class RAGState(TypedDict):
    repo_url: str
    valid: bool
    error: str
    chunks: list
    embeddings: list
    collection_name: str
    chat_history: List[Dict[str, str]]
    answer: str
    owner: str
    repo: str
    mode: str  # "process_repo" or "chat_only"
    processed: bool
def sanitize_collection_name(owner, repo):
    """
    Sanitize collection name to meet ChromaDB requirements:
    1. 3-63 characters
    2. Start and end with alphanumeric
    3. Only alphanumeric, underscores, or hyphens (but ChromaDB actually doesn't allow hyphens)
    4. No consecutive periods
    5. Not a valid IPv4 address
    """
    # Combine owner and repo with underscore
    raw_name = f"{owner}_{repo}"
    
    # Replace hyphens with underscores (ChromaDB doesn't like hyphens)
    sanitized = raw_name.replace('-', '_')
    
    # Remove any characters that aren't alphanumeric or underscore
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
    
    # Ensure it starts and ends with alphanumeric
    sanitized = sanitized.strip('_')
    
    # Truncate if too long (leave room for potential suffix if needed)
    if len(sanitized) > 60:
        sanitized = sanitized[:60]
    
    # Ensure minimum length
    if len(sanitized) < 3:
        sanitized = sanitized + '_collection'
    
    # Ensure it ends with alphanumeric
    if sanitized.endswith('_'):
        sanitized = sanitized[:-1] + 'x'
    
    return sanitized
def validate_url_node(state):
    """
    Checks if the input is a valid GitHub URL and extracts owner/repo.

    Args:
        state (dict): Current agent state

    Returns:
        dict: Updated state with owner/repo or error
    """
    import re
    url = state["repo_url"]
    pattern = r"^https://github.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    if match:
        return {
            "valid": True, 
            "owner": match.group(1), 
            "repo": match.group(2),
            "error": ""
        }
    else:
        return {"valid": False, "error": "Invalid GitHub URL"}

def process_repo_node(state):
    """
    Crawls the repo, chunks code, generates embeddings, and stores them.

    Args:
        state (dict): Current agent state

    Returns:
        dict: Updated state with chunks, embeddings, and collection name
    """
    try:


        owner, repo = state["owner"], state["repo"]
        
        # Initialize components
        crawler = GitHubRepoCrawler(token=GITHUB_TOKEN)
        files = crawler.get_files(owner, repo)
        # code_files = [f for f in files if crawler.is_code_file(f['path'])]
        code_files = [f for f in files] #Include also files which are not code: README.md and so on

        if not code_files:
            return {"error": "No code files found in the repository", "valid": False}
        
        # Chunk the code
        chunker = CodeChunker()
        all_chunks = []
        # repo_info = {'owner': owner, 'repo': repo}
        
        for file_info in code_files:
            content = crawler.get_file_content(owner, repo, file_info['path'])
            if content:  # Only process if content exists
                all_chunks.extend(chunker.chunk_by_lines(content, file_info['path'], owner, repo))
        
        if not all_chunks:
            return {"error": "No content could be extracted from the repository", "valid": False}
        
        # Generate embeddings
        embedder = EmbeddingGenerator(api_key=OPENAI_API_KEY)
        embeddings = embedder.generate_batch_embeddings([c['content'] for c in all_chunks])
        
        # Store in vector database
        chroma = ChromaDBManager(persist_directory=CHROMA_DB_DIR)
        collection_name = sanitize_collection_name(owner, repo)
        collection = chroma.create_or_get_collection(collection_name)
        chroma.store_chunks(collection, all_chunks, embeddings)
        
        return {
            "chunks": all_chunks, 
            "embeddings": embeddings, 
            "collection_name": collection_name,
            "processed": True,
            "error": ""
        }
    
    except Exception as e:
        return {"error": f"Error processing repository: {str(e)}", "valid": False}

def chat_node(state):
    """
    Handles a chat query: retrieves similar code and asks GPT-4o mini for an answer.

    Args:
        state (dict): Current agent state

    Returns:
        dict: Updated state with the answer
    """
    try:
        

        # Get the latest user message
        if not state.get("chat_history") or len(state["chat_history"]) == 0:
            # return {"error": "No chat history found", "answer": "Please ask a question."}
                        # Return a welcome message instead of an error
            welcome_message = f"Hello! I'm ready to help you with questions about the {state.get('owner', '')}/{state.get('repo', '')} repository. What would you like to know?"
            
            return {
                "answer": welcome_message,
                "chat_history": [{"role": "assistant", "content": welcome_message}],
                "error": ""
            }
        
        query = state["chat_history"][-1]["content"]
        
        # Generate query embedding
        embedder = EmbeddingGenerator(api_key=OPENAI_API_KEY)
        query_embedding = embedder.generate_embedding(query)
        
        # Retrieve similar code chunks
        chroma = ChromaDBManager(persist_directory=CHROMA_DB_DIR)
        collection = chroma.create_or_get_collection(state["collection_name"])
        results = chroma.query_similar_code(collection, query_embedding, n_results=5)
        
        # Prepare context from retrieved chunks
        context = "\n\n".join([doc for doc in results['documents'][0]])
        
        # Prepare conversation history for context
        conversation_context = ""
        if len(state["chat_history"]) > 1:
            recent_history = state["chat_history"][-6:]  # Last 3 exchanges
            for i, msg in enumerate(recent_history[:-1]):  # Exclude current query
                if msg["role"] == "user":
                    conversation_context += f"Previous Question: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    conversation_context += f"Previous Answer: {msg['content']}\n"
        
        # Generate response using OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        system_prompt = f"""You are a helpful codebase assistant for the GitHub repository {state.get('owner', '')}/{state.get('repo', '')}. 
        
Your task is to answer questions about the codebase using the provided context from the repository's code.

Guidelines:
- Provide clear, concise answers based on the code context
- Include relevant code snippets when helpful
- If the context doesn't contain enough information to answer the question, say so
- Reference specific files or functions when relevant
- Be conversational and helpful
- Consider the conversation history when providing context-aware responses"""

        user_prompt = f"""Context from codebase:
{context}

{conversation_context}

Current Question: {query}

Please provide a helpful answer based on the codebase context."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Update chat history with assistant response
        updated_history = state["chat_history"].copy()
        updated_history.append({"role": "assistant", "content": answer})
        
        return {
            "answer": answer,
            "chat_history": updated_history,
            "error": ""
        }
    
    except Exception as e:
        return {"error": f"Error in chat: {str(e)}", "answer": "Sorry, I encountered an error while processing your question."}

def route_after_validation(state):
    """Route based on whether URL is valid and what mode we're in"""
    if not state.get("valid", False):
        return END
    
    if state.get("mode") == "chat_only":
        return "chat"
    else:
        return "process_repo"

def route_after_processing(state):
    """Route after repo processing"""
    if state.get("error"):
        return END
    return "chat"

def build_graph():
    """
    Builds and returns the LangGraph agent workflow.
    """
    builder = StateGraph(RAGState)
    
    # Add nodes
    builder.add_node("validate_url", validate_url_node)
    builder.add_node("process_repo", process_repo_node)
    builder.add_node("chat", chat_node)
    
    # Add edges
    builder.add_edge(START, "validate_url")
    
    builder.add_conditional_edges(
        "validate_url",
        route_after_validation,
        {
            "process_repo": "process_repo",
            "chat": "chat",
            END: END
        }
    )
    # Route after processing
    builder.add_conditional_edges(
        "process_repo",
        route_after_processing,
        {
            "chat": "chat",
            END: END
        }
    )
    
    # Chat ends the workflow
    builder.add_edge("chat", END)
    
    return builder.compile()

def create_chat_only_state(collection_name: str, owner: str, repo: str, chat_history: List[Dict[str, str]]):
    """
    Create a state for chat-only mode (when repo is already processed)
    """
    return {
        "repo_url": f"https://github.com/{owner}/{repo}",
        "valid": True,
        "error": "",
        "chunks": [],
        "embeddings": [],
        "collection_name": collection_name,
        "chat_history": chat_history,
        "answer": "",
        "owner": owner,
        "repo": repo,  
        "mode": "chat_only",
        "processed": True
    }

# """
# agent.py

# Defines the LangGraph agent workflow for the RAG application:
# 1. Validates the GitHub URL.
# 2. Crawls, chunks, embeds, and stores the repo.
# 3. Handles chat queries using retrieval-augmented generation.
# """

# from langgraph.graph import StateGraph, START
# from typing_extensions import TypedDict

# class RAGState(TypedDict):
#     repo_url: str
#     valid: bool
#     error: str
#     chunks: list
#     embeddings: list
#     collection_name: str
#     chat_history: list
#     answer: str

# def validate_url_node(state):
#     """
#     Checks if the input is a valid GitHub URL and extracts owner/repo.

#     Args:
#         state (dict): Current agent state

#     Returns:
#         dict: Updated state with owner/repo or error
#     """
#     import re
#     url = state["repo_url"]
#     pattern = r"^https://github.com/([^/]+)/([^/]+)"
#     match = re.match(pattern, url)
#     if match:
#         return {"valid": True, "owner": match.group(1), "repo": match.group(2)}
#     else:
#         return {"valid": False, "error": "Invalid GitHub URL"}

# def process_repo_node(state):
#     """
#     Crawls the repo, chunks code, generates embeddings, and stores them.

#     Args:
#         state (dict): Current agent state

#     Returns:
#         dict: Updated state with chunks, embeddings, and collection name
#     """
#     from .settings import OPENAI_API_KEY, GITHUB_TOKEN, CHROMA_DB_DIR
#     from .repo_crawler import GitHubRepoCrawler
#     from .chunker import CodeChunker
#     from .embedder import EmbeddingGenerator
#     from .vector_store import ChromaDBManager

#     owner, repo = state["owner"], state["repo"]
#     crawler = GitHubRepoCrawler(token=GITHUB_TOKEN)
#     files = crawler.get_files(owner, repo)
#     code_files = [f for f in files if crawler.is_code_file(f['path'])]
#     chunker = CodeChunker()
#     all_chunks = []
#     repo_info = {'owner': owner, 'repo': repo}
#     for file_info in code_files:
#         content = crawler.get_file_content(owner, repo, file_info['path'])
#         all_chunks.extend(chunker.chunk_by_lines(content, file_info['path'], repo_info))
#     embedder = EmbeddingGenerator(api_key=OPENAI_API_KEY)
#     embeddings = embedder.generate_batch_embeddings([c['content'] for c in all_chunks])
#     chroma = ChromaDBManager(persist_directory=CHROMA_DB_DIR)
#     collection_name = f"{owner}_{repo}"
#     collection = chroma.create_or_get_collection(collection_name)
#     chroma.store_chunks(collection, all_chunks, embeddings)
#     return {"chunks": all_chunks, "embeddings": embeddings, "collection_name": collection_name}

# def chat_node(state):
#     """
#     Handles a chat query: retrieves similar code and asks GPT-4o mini for an answer.

#     Args:
#         state (dict): Current agent state

#     Returns:
#         dict: Updated state with the answer
#     """
#     from .settings import OPENAI_API_KEY, CHROMA_DB_DIR
#     from .embedder import EmbeddingGenerator
#     from .vector_store import ChromaDBManager
#     from openai import OpenAI

#     query = state["chat_history"][-1]["content"]
#     embedder = EmbeddingGenerator(api_key=OPENAI_API_KEY)
#     query_embedding = embedder.generate_embedding(query)
#     chroma = ChromaDBManager(persist_directory=CHROMA_DB_DIR)
#     collection = chroma.create_or_get_collection(state["collection_name"])
#     results = chroma.query_similar_code(collection, query_embedding)
#     context = "\n\n".join([doc for doc in results['documents'][0]])
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a codebase assistant."},
#             {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
#         ]
#     )
#     return {"answer": response.choices[0].message.content}

# def build_graph():
#     """
#     Builds and returns the LangGraph agent workflow.
#     """
#     builder = StateGraph(RAGState)
#     builder.add_node("validate_url", validate_url_node)
#     builder.add_node("process_repo", process_repo_node)
#     builder.add_node("chat", chat_node)
#     builder.add_edge(START, "validate_url")
#     builder.add_edge("validate_url", "process_repo", condition=lambda s: s["valid"])
#     builder.add_edge("process_repo", "chat")
#     builder.set_entry_point("validate_url")
#     builder.set_finish_point("chat")
#     return builder.compile()
