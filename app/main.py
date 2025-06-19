"""
main.py
Streamlit UI for the RAG GitHub application.
- Step 1: User enters a GitHub repo URL.
- Step 2: Repo is processed (crawled, chunked, embedded, indexed).
- Step 3: User can chat with the codebase using GPT-4o mini.
"""

import streamlit as st
from agent import build_graph, create_chat_only_state
import time

# Page configuration
st.set_page_config(
    page_title="GitHub RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    .status-success {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .status-error {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if "graph" not in st.session_state:
        st.session_state.graph = build_graph()
    
    if "current_state" not in st.session_state:
        st.session_state.current_state = {
            "repo_url": "",
            "chat_history": [],
            "collection_name": "",
            "owner": "",
            "repo": "",
            "processed": False,
            "valid": False,
            "error": ""
        }
    
    if "processing" not in st.session_state:
        st.session_state.processing = False

def reset_session():
    """Reset the session to start fresh"""
    st.session_state.current_state = {
        "repo_url": "",
        "chat_history": [],
        "collection_name": "",
        "owner": "",
        "repo": "",
        "processed": False,
        "valid": False,
        "error": ""
    }
    st.session_state.processing = False

def display_chat_history():
    """Display the chat history in a nice format"""
    if st.session_state.current_state.get("chat_history"):
        for i, message in enumerate(st.session_state.current_state["chat_history"]):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])

def process_repository(repo_url):
    """Process the repository with proper error handling"""
    try:
        # Create initial state for processing
        initial_state = {
            "repo_url": repo_url,
            "chat_history": [],
            "mode": "process_repo",
            "valid": False,
            "processed": False,
            "error": ""
        }
        
        # Show processing status
        status_container = st.empty()
        status_container.info("🔄 Processing repository... This may take a few minutes.")
        
        # Process the repository
        result = st.session_state.graph.invoke(initial_state)
        
        # Update session state based on result
        if result.get("error"):
            st.session_state.current_state.update({
                "error": result["error"],
                "processed": False,
                "valid": False
            })
            status_container.error(f"❌ Error: {result['error']}")
            return False
        
        elif result.get("processed"):
            st.session_state.current_state.update({
                "repo_url": repo_url,
                "collection_name": result["collection_name"],
                "owner": result["owner"],
                "repo": result["repo"],
                "processed": True,
                "valid": True,
                "error": "",
                "chat_history": []
            })
            status_container.success("✅ Repository processed successfully! You can now ask questions about the codebase.")
            return True
        
        else:
            st.session_state.current_state.update({
                "error": "Unknown error occurred during processing",
                "processed": False,
                "valid": False
            })
            status_container.error("❌ Unknown error occurred during processing")
            return False
            
    except Exception as e:
        error_msg = f"Error processing repository: {str(e)}"
        st.session_state.current_state.update({
            "error": error_msg,
            "processed": False,
            "valid": False
        })
        st.error(f"❌ {error_msg}")
        return False

def handle_chat_query(query):
    """Handle a chat query with proper state management"""
    try:
        # Add user message to chat history
        current_history = st.session_state.current_state.get("chat_history", [])
        current_history.append({"role": "user", "content": query})
        
        # Create chat state
        chat_state = create_chat_only_state(
            collection_name=st.session_state.current_state["collection_name"],
            owner=st.session_state.current_state["owner"],
            repo=st.session_state.current_state["repo"],
            chat_history=current_history
        )
        
        # Get response from the agent
        with st.spinner("🤔 Thinking..."):
            result = st.session_state.graph.invoke(chat_state)
        
        # Update session state with the result
        if result.get("error"):
            st.error(f"Error: {result['error']}")
            return
            
        # Update chat history with both user query and assistant response
        st.session_state.current_state["chat_history"] = result.get("chat_history", current_history)
        
    except Exception as e:
        st.error(f"Error handling chat query: {str(e)}")

# Main app
def main():
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🤖 GitHub RAG Chatbot")
    st.markdown("Chat with any GitHub repository using AI")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar for repository management
    with st.sidebar:
        st.header("Repository Settings")
        
        # Show current repository status
        if st.session_state.current_state.get("processed"):
            st.success(f"📁 Active Repository:")
            st.write(f"**{st.session_state.current_state['owner']}/{st.session_state.current_state['repo']}**")
            
            if st.button("🔄 Process New Repository", use_container_width=True):
                reset_session()
                st.rerun()
        
        st.markdown("---")
        
        # Repository URL input
        repo_url = st.text_input(
            "GitHub Repository URL:",
            value=st.session_state.current_state.get("repo_url", ""),
            placeholder="https://github.com/owner/repo",
            help="Enter a valid GitHub repository URL"
        )
        
        # Process repository button
        if st.button("🚀 Process Repository", use_container_width=True, disabled=st.session_state.processing):
            if repo_url:
                st.session_state.processing = True
                success = process_repository(repo_url)
                st.session_state.processing = False
                if success:
                    st.rerun()
            else:
                st.error("Please enter a repository URL")
        
        # Show processing status
        if st.session_state.processing:
            st.warning("⏳ Processing in progress...")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show current status
        if st.session_state.current_state.get("error"):
            st.error(f"❌ {st.session_state.current_state['error']}")
        
        elif not st.session_state.current_state.get("processed"):
            st.info("👈 Please enter a GitHub repository URL in the sidebar and click 'Process Repository' to get started.")
        
        else:
            # Chat interface
            st.subheader(f"💬 Chat with {st.session_state.current_state['owner']}/{st.session_state.current_state['repo']}")
            
            # Display chat history
            display_chat_history()
            
            # Chat input
            if query := st.chat_input("Ask a question about the codebase..."):
                handle_chat_query(query)
                st.rerun()
    
    with col2:
        # Help and information panel
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        1. **Enter Repository URL**: Paste a GitHub repository URL in the sidebar
        2. **Process Repository**: Click the process button to analyze the code
        3. **Start Chatting**: Once processed, ask questions about the codebase
        
        **Example Questions:**
        - "What does this repository do?"
        - "How is the code organized?"
        - "Show me the main functions"
        - "Explain the API endpoints"
        - "What are the dependencies?"
        """)
        
        # Repository statistics (if available)
        if st.session_state.current_state.get("processed"):
            st.subheader("📊 Repository Info")
            st.write(f"**Owner:** {st.session_state.current_state['owner']}")
            st.write(f"**Repository:** {st.session_state.current_state['repo']}")
            st.write(f"**Collection:** {st.session_state.current_state['collection_name']}")
            
            # Chat statistics
            chat_count = len([msg for msg in st.session_state.current_state.get("chat_history", []) if msg["role"] == "user"])
            st.write(f"**Questions Asked:** {chat_count}")

if __name__ == "__main__":
    main()

# """
# main.py

# Streamlit UI for the RAG GitHub application.
# - Step 1: User enters a GitHub repo URL.
# - Step 2: Repo is processed (crawled, chunked, embedded, indexed).
# - Step 3: User can chat with the codebase using GPT-4o mini.
# """

# import streamlit as st
# from app.agent import build_graph

# st.title("GitHub RAG Chatbot")

# # Initialize LangGraph agent and state in session
# if "graph" not in st.session_state:
#     st.session_state.graph = build_graph()
# if "state" not in st.session_state:
#     st.session_state.state = {"repo_url": "", "chat_history": []}

# # Step 1: Input GitHub repo URL
# repo_url = st.text_input("Enter GitHub repository URL:", value=st.session_state.state.get("repo_url", ""))
# if st.button("Process Repository"):
#     st.session_state.state["repo_url"] = repo_url
#     result = st.session_state.graph.invoke(st.session_state.state)
#     if not result.get("valid", True):
#         st.error(result.get("error", "Unknown error"))
#     else:
#         st.success("Repository processed and indexed!")

# # Step 2: Chat interface (after successful processing)
# if "collection_name" in st.session_state.state:
#     st.subheader("Ask questions about the codebase:")
#     user_query = st.chat_input("Type your question...")
#     if user_query:
#         st.session_state.state["chat_history"].append({"role": "user", "content": user_query})
#         result = st.session_state.graph.invoke(st.session_state.state)
#         st.chat_message("assistant").write(result["answer"])
