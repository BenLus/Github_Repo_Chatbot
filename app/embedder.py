"""
embedder.py

Generates vector embeddings for code chunks using OpenAI's embedding API.
"""

from openai import OpenAI

class EmbeddingGenerator:
    """
    Handles embedding generation for code chunks using OpenAI.
    """
    def __init__(self, api_key, model="text-embedding-3-small"):
        """
        Args:
            api_key (str): OpenAI API key
            model (str): Embedding model name
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_embedding(self, text):
        """
        Generates an embedding for a single text.

        Args:
            text (str): The text to embed

        Returns:
            list: Embedding vector
        """
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def generate_batch_embeddings(self, texts, batch_size=20):
        """
        Generates embeddings for a batch of texts.

        Args:
            texts (list): List of strings to embed
            batch_size (int): How many texts to embed per API call

        Returns:
            list: List of embedding vectors
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(model=self.model, input=batch)
            embeddings.extend([item.embedding for item in response.data])
        return embeddings
