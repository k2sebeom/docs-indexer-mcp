import os
import json
import shutil
from datetime import datetime
from typing import List, Tuple
import requests

import html2text

from docs_indexer_mcp.models import Documentation


class DocumentManager:
    BASE_DIR = os.path.expanduser("~/.docs_indexer")
    DOCS_DIR = os.path.join(BASE_DIR, "docs")

    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False

    @classmethod
    def ensure_dirs(cls):
        """Ensure that the necessary directories exist."""
        os.makedirs(cls.DOCS_DIR, exist_ok=True)

    @classmethod
    def get_doc_dir(cls, doc_name: str) -> str:
        """Get the directory for a specific documentation."""
        return os.path.join(cls.DOCS_DIR, doc_name)

    @classmethod
    def get_meta_path(cls, doc_name: str) -> str:
        """Get the path to the meta.json file for a documentation."""
        return os.path.join(cls.get_doc_dir(doc_name), "meta.json")

    @classmethod
    def list_docs(cls) -> List[str]:
        """List all available documentations."""
        if not os.path.exists(cls.DOCS_DIR):
            return []

        docs = []
        for doc_name in os.listdir(cls.DOCS_DIR):
            doc_path = os.path.join(cls.DOCS_DIR, doc_name)
            meta_path = os.path.join(doc_path, "meta.json")
            if os.path.isdir(doc_path) and os.path.exists(meta_path):
                docs.append(doc_name)

        return docs

    @classmethod
    def save_documentation(cls, doc: Documentation):
        """Save documentation to meta.json."""
        # Ensure directory exists
        doc_dir = cls.get_doc_dir(doc.name)
        os.makedirs(doc_dir, exist_ok=True)

        # Set last_synced if not already set
        if not doc.last_synced:
            doc.last_synced = datetime.now().isoformat()

        # Save meta.json
        meta_path = cls.get_meta_path(doc.name)
        with open(meta_path, "w") as f:
            json.dump(doc.to_dict(), f, indent=2)

        return meta_path

    @classmethod
    def load_documentation(cls, doc_name: str) -> Documentation:
        """Load documentation from meta.json."""
        meta_path = cls.get_meta_path(doc_name)

        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Documentation '{doc_name}' not found")

        with open(meta_path, "r") as f:
            data = json.load(f)

        return Documentation.from_dict(data)

    @classmethod
    def delete_documentation(cls, doc_name: str) -> bool:
        """Delete a documentation by removing its directory.
        
        Args:
            doc_name: Name of the documentation to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
            
        Raises:
            FileNotFoundError: If documentation not found
        """
        doc_dir = cls.get_doc_dir(doc_name)
        
        if not os.path.exists(doc_dir):
            raise FileNotFoundError(f"Documentation '{doc_name}' not found")
            
        try:
            shutil.rmtree(doc_dir)
            return True
        except Exception as e:
            print(f"Error deleting documentation: {e}")
            return False
    
    @classmethod
    def read_page(cls, doc_name: str, url: str) -> Tuple[str, str]:
        """Read a specific page from documentation and convert to text.

        Args:
            doc_name: Name of the documentation
            url: URL of the page to read

        Returns:
            Tuple of (title, text_content)

        Raises:
            FileNotFoundError: If documentation not found
            ValueError: If no page found with the given URL
            requests.RequestException: If page cannot be fetched
        """
        documentation = DocumentManager.load_documentation(doc_name)
        
        # Find the page with matching URL
        matching_pages = [p for p in documentation.pages if p.url == url]
        if not matching_pages:
            raise ValueError(f"No page found with URL: {url}")
        page = matching_pages[0]

        response = requests.get(page.url)
        response.raise_for_status()

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        text_content = converter.handle(response.text)

        return page.title, text_content
