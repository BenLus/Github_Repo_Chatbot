"""
settings.py

Loads environment variables and API keys for the application.
"""

import os
from dotenv import load_dotenv

# Load .env file variables into environment
load_dotenv()

# OpenAI API key for embedding and chat
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# GitHub token for authenticated API access (optional, increases rate limits)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Directory where ChromaDB will persist its data
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
