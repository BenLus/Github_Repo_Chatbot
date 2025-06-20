"""
chunker.py

Splits code files into manageable chunks for embedding, using token limits and overlap.
"""

import tiktoken

class CodeChunker:
    """
    Splits code into chunks of a specified token size, with optional overlap.
    """
    def __init__(self, max_chunk_size=1000, chunk_overlap=100):
        """
        Args:
            max_chunk_size (int): Maximum tokens per chunk
            chunk_overlap (int): Number of tokens to overlap between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("o200k_base")  # GPT-4o mini tokenizer

    def count_tokens(self, text):
        """
        Counts the number of tokens in a string.

        Args:
            text (str): The text to tokenize

        Returns:
            int: Number of tokens
        """
        return len(self.encoding.encode(text))

    def chunk_by_lines(self, content, file_path, owner,repo):
        """
        Chunks code content by lines, keeping each chunk within the token limit.

        Args:
            content (str): File content to chunk
            file_path (str): Path to the file
            owner (str): Owner of the repository
            repo (str): Repository's name

        Returns:
            list: List of chunk dicts with content and metadata
        """
        lines = content.split('\n')
        chunks, current_chunk, current_tokens, start_line = [], [], 0, 1
        for i, line in enumerate(lines, 1):
            line_tokens = self.count_tokens(line + '\n')
            if current_tokens + line_tokens > self.max_chunk_size and current_chunk:
                chunk_content = '\n'.join(current_chunk)
                chunks.append({
                    "content": chunk_content,
                    "file_path": file_path,
                    "start_line": start_line,
                    "end_line": i - 1,
                    "owner": owner,
                    "repo": repo
                })
                overlap_lines = current_chunk[-self.chunk_overlap:] if self.chunk_overlap else []
                current_chunk = overlap_lines + [line]
                current_tokens = sum(self.count_tokens(l + '\n') for l in current_chunk)
                start_line = i - len(overlap_lines)
            else:
                current_chunk.append(line)
                current_tokens += line_tokens
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            chunks.append({
                "content": chunk_content,
                "file_path": file_path,
                "start_line": start_line,
                "end_line": len(lines),
                "owner": owner,
                "repo": repo
            })
        return chunks
