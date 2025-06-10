import sys
import requests
from typing import List

from .document_manager import DocumentManager
from .crawler import Crawler


class CLI:
    def __init__(self):
        DocumentManager.ensure_dirs()
        self.commands = {
            "help": self.show_help,
            "exit": self.exit,
            "crawl": self.crawl,
            "list": self.list_docs,
            "pages": self.list_pages,
            "read": self.read_page,
        }
    
    def show_help(self, args: List[str] = None) -> None:
        """Show help information."""
        print("Available commands:")
        print("  help                     - Show this help message")
        print("  exit                     - Exit the program")
        print("  crawl <title> <url> <prefix> - Crawl and index a documentation")
        print("  list                     - List all available documentations")
        print("  pages <doc_name>         - List all pages in a documentation")
        print("  read <doc_name> <page_number> - Read a specific page from documentation")
    
    def exit(self, args: List[str] = None) -> None:
        """Exit the program."""
        print("Goodbye!")
        sys.exit(0)
    
    def crawl(self, args: List[str]) -> None:
        """Crawl and index a documentation."""
        if len(args) < 3:
            print("Usage: crawl <title> <url> <prefix>")
            return
        
        doc_name, base_url, prefix = args
        print(f"Crawling {base_url} with prefix {prefix}...")
        
        crawler = Crawler(doc_name, base_url, prefix)
        crawler.crawl()
    
    def list_docs(self, args: List[str] = None) -> None:
        """List all available documentations."""
        docs = DocumentManager.list_docs()
        
        if not docs:
            print("No documentations available.")
            return
        
        print("Available documentations:")
        for doc in docs:
            try:
                documentation = DocumentManager.load_documentation(doc)
                print(f"  {doc} - {len(documentation.pages)} pages, last synced: {documentation.last_synced}")
            except Exception as e:
                print(f"  {doc} - Error loading documentation: {e}")
    
    def list_pages(self, args: List[str]) -> None:
        """List all pages in a documentation."""
        if not args:
            print("Usage: pages <doc_name>")
            return
        
        doc_name = args[0]
        
        try:
            documentation = DocumentManager.load_documentation(doc_name)
            print(f"Pages in {doc_name} ({len(documentation.pages)}):")
            
            for i, page in enumerate(documentation.pages, 1):
                print(f"  {i}. {page.title}")
                print(f"     {page.url}")
        except FileNotFoundError:
            print(f"Documentation '{doc_name}' not found.")
        except Exception as e:
            print(f"Error loading documentation: {e}")
    
    def read_page(self, args: List[str]) -> None:
        """Read a specific page from documentation."""
        if len(args) < 2:
            print("Usage: read <doc_name> <page_number>")
            return
        
        doc_name = args[0]
        
        try:
            page_num = int(args[1])
            
            # Convert from 1-based (user-facing) to 0-based (internal) indexing
            page_index = page_num - 1
            
            try:
                title, content = Crawler.read_page(doc_name, page_index)
                print(f"\n=== {title} ===\n")
                print(content)
            except IndexError:
                documentation = DocumentManager.load_documentation(doc_name)
                print(f"Invalid page number. Available pages: 1-{len(documentation.pages)}")
            except requests.RequestException as e:
                print(f"Error fetching page content: {e}")
                
        except ValueError:
            print("Page number must be an integer.")
        except FileNotFoundError:
            print(f"Documentation '{doc_name}' not found.")
        except Exception as e:
            print(f"Error: {e}")
    
    def run_command(self, command: str, args: List[str]) -> None:
        """Run a command with arguments."""
        if command in self.commands:
            self.commands[command](args)
        else:
            print(f"Unknown command: {command}")
            self.show_help()
    
    def run(self) -> None:
        """Run the CLI loop."""
        print("Welcome to Docs Indexer!")
        print("Type 'help' for available commands.")
        
        while True:
            try:
                user_input = input(">>> ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                self.run_command(command, args)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit the program.")
            except Exception as e:
                print(f"Error: {e}")


def main() -> None:
    cli = CLI()
    cli.run()