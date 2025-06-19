"""
vector_store.py

Handles storing and retrieving code embeddings using ChromaDB.
"""

import chromadb

class ChromaDBManager:
    """
    Manages ChromaDB collections for storing and querying code embeddings.
    """
    def __init__(self, persist_directory="./chroma_db"):
        """
        Args:
            persist_directory (str): Directory for ChromaDB data
        """
        self.client = chromadb.PersistentClient(path=persist_directory)

    def create_or_get_collection(self, collection_name):
        """
        Gets or creates a ChromaDB collection.

        Args:
            collection_name (str): Name of the collection

        Returns:
            chromadb.Collection: The collection object
        """
        try:
            return self.client.get_collection(collection_name)
        except Exception:
            # Create collection if it doesn't exist
            return self.client.create_collection(name=collection_name, embedding_function=None)

    def store_chunks(self, collection, chunks, embeddings):
        """
        Stores code chunks and their embeddings in ChromaDB.

        Args:
            collection (chromadb.Collection): The collection to store in
            chunks (list): List of chunk dicts
            embeddings (list): List of embedding vectors
        """
        ids = [f"{chunk['file_path']}_{chunk['start_line']}_{chunk['end_line']}" for chunk in chunks]
        documents = [chunk['content'] for chunk in chunks]
        metadatas = [chunk for chunk in chunks]
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        # # Check total count
        # print(f"Total items in collection: {collection.count()}")

        # # Or get all IDs to see if there are actual duplicates
        # all_results = collection.get()
        # all_ids = all_results['ids']
        # print(f"Unique IDs: {len(set(all_ids))}")
        # print(f"Total IDs: {len(all_ids)}")

        # # If these numbers are different, you have duplicates
        # if len(set(all_ids)) != len(all_ids):
        #     print("You have duplicate IDs!")
        # else:
        #     print("No duplicates - ChromaDB rejected the duplicate adds")
    def query_similar_code(self, collection, query_embedding, n_results=5):
        """
        Queries ChromaDB for code chunks similar to the query embedding.

        Args:
            collection (chromadb.Collection): The collection to query
            query_embedding (list): The embedding to search with
            n_results (int): Number of results to return

        Returns:
            dict: Query results from ChromaDB
        """
        return collection.query(query_embeddings=[query_embedding], n_results=n_results)
