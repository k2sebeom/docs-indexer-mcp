import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from typing import Set, List
import time
from datetime import datetime

from .models import Documentation, Page
from .config import Config


class Crawler:
    def __init__(self, doc_name: str, base_url: str, prefix: str):
        self.doc_name = doc_name
        self.base_url = base_url
        self.prefix = prefix
        self.visited_urls: Set[str] = set()
        self.pages: List[Page] = []
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and query parameters."""
        parsed = urlparse(url)
        # Remove query parameters and fragments
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return clean_url
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and starts with the prefix."""
        normalized = self.normalize_url(url)
        return normalized.startswith(self.prefix)
    
    def crawl(self):
        """Start crawling from the base URL."""
        self._crawl_page(self.base_url)
        self._save_results()
    
    def _crawl_page(self, url: str):
        """Crawl a single page and its links."""
        normalized_url = self.normalize_url(url)
        
        # Skip if already visited
        if normalized_url in self.visited_urls:
            return
        
        self.visited_urls.add(normalized_url)
        
        try:
            print(f'Indexing {url}')
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')

            
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else normalized_url
            
            # Add page to results
            self.pages.append(Page(title=title, url=normalized_url))
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                
                # Remove fragment
                absolute_url = urldefrag(absolute_url)[0]
                
                if self.is_valid_url(absolute_url):
                    self._crawl_page(absolute_url)
                    
        except Exception as e:
            print(f"Error crawling {url}: {e}")
    
    def _save_results(self):
        """Save crawling results to meta.json."""
        doc = Documentation(
            name=self.doc_name,
            base_url=self.base_url,
            prefix=self.prefix,
            pages=self.pages,
            last_synced=datetime.now().isoformat()
        )
        
        # Ensure directory exists
        doc_dir = Config.get_doc_dir(self.doc_name)
        os.makedirs(doc_dir, exist_ok=True)
        
        # Save meta.json
        meta_path = Config.get_meta_path(self.doc_name)
        with open(meta_path, 'w') as f:
            json.dump(doc.to_dict(), f, indent=2)
        
        print(f"Indexed {len(self.pages)} pages for {self.doc_name}")


def load_documentation(doc_name: str) -> Documentation:
    """Load documentation from meta.json."""
    meta_path = Config.get_meta_path(doc_name)
    
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Documentation '{doc_name}' not found")
    
    with open(meta_path, 'r') as f:
        data = json.load(f)
    
    return Documentation.from_dict(data)