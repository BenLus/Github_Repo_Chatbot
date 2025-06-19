"""
repo_crawler.py

Handles crawling a GitHub repository: listing files and fetching file contents.
"""

import requests
from pathlib import Path

class GitHubRepoCrawler:
    """
    Interacts with the GitHub API to list and fetch files from a repository.
    """
    def __init__(self, token=None):
        """
        Args:
            token (str): GitHub personal access token (optional)
        """
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'token {token}'})
        self.session.headers.update({'Accept': 'application/vnd.github.v3+json'})

    def get_files(self, owner, repo, branch="main"):
        """
        Lists all files in a GitHub repository branch.

        Args:
            owner (str): Repository owner
            repo (str): Repository name
            branch (str): Branch name (default: main)

        Returns:
            list: List of file metadata dicts
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        resp = self.session.get(url)
        resp.raise_for_status()
        # Only return files (blobs), not directories (trees)
        return [item for item in resp.json()['tree'] if item['type'] == 'blob']

    def get_file_content(self, owner, repo, file_path, branch="main"):
        """
        Fetches the raw content of a file from a GitHub repository.

        Args:
            owner (str): Repository owner
            repo (str): Repository name
            file_path (str): Path to the file in the repo
            branch (str): Branch name

        Returns:
            str: File content as text
        """
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.text

    def is_code_file(self, file_path):
        """
        Determines if a file is likely to be code based on its extension.

        Args:
            file_path (str): Path to the file

        Returns:
            bool: True if file is a code file
        """
        code_exts = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.sh', '.html', '.css', '.json', '.yaml', '.yml', '.sql'}
        return Path(file_path).suffix.lower() in code_exts
