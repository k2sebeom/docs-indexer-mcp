import os
import json
from datetime import datetime
from typing import List

from .models import Documentation, Page


class DocumentManager:
    BASE_DIR = os.path.expanduser("~/.docs_indexer")
    DOCS_DIR = os.path.join(BASE_DIR, "docs")

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
    def list_docs(cls) -> list:
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
        with open(meta_path, 'w') as f:
            json.dump(doc.to_dict(), f, indent=2)
        
        return meta_path

    @classmethod
    def load_documentation(cls, doc_name: str) -> Documentation:
        """Load documentation from meta.json."""
        meta_path = cls.get_meta_path(doc_name)
        
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Documentation '{doc_name}' not found")
        
        with open(meta_path, 'r') as f:
            data = json.load(f)
        
        return Documentation.from_dict(data)