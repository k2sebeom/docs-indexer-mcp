import os
import json
from pathlib import Path


class Config:
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