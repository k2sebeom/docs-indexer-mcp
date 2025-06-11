# Docs Indexer MCP

A documentation indexing and reading tool that works both as a standalone CLI application and as an MCP (Model Context Protocol) server for AI assistants.

## Overview

Docs Indexer MCP allows you to:

1. Crawl and index web-based documentation
2. List available documentation sets
3. Browse pages within documentation
4. Read documentation content in markdown format
5. Integrate with AI assistants via MCP

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/docs-indexer-mcp.git
cd docs-indexer-mcp

uv run cli
```

## Usage

### CLI Mode

The tool can be used as a standalone command-line application:

```bash
# Start the CLI
uv run cli
```

Available commands:

- `help` - Show help information
- `exit` - Exit the program
- `crawl <title> <url> <prefix>` - Crawl and index a documentation
- `list` - List all available documentations
- `pages <doc_name>` - List all pages in a documentation
- `read <doc_name> <page_number>` - Read a specific page from documentation

Example workflow:

```bash
# Crawl and index Python documentation
>>> crawl python https://docs.python.org/3/ https://docs.python.org/3/

# List available documentations
>>> list

# List pages in Python documentation
>>> pages python

# Read a specific page (page number 5)
>>> read python 5
```

### MCP Server Mode

The tool can also run as an MCP server to provide documentation access to AI assistants:

```bash
# Start the MCP server
uv run docs-indexer-mcp
```

When running as an MCP server, the following tools are available to AI assistants:

- `list_documentations` - List all available documentations
- `list_pages` - List available pages in a documentation
- `read_page` - Read a specific page from documentation

## Data Storage

All indexed documentation is stored in `~/.docs_indexer/docs/` with the following structure:

```
~/.docs_indexer/
  └── docs/
      └── <doc_name>/
          └── meta.json
```

Each `meta.json` file contains:
- Documentation name
- Base URL
- URL prefix for crawling
- List of pages with titles and URLs
- Last sync timestamp

## Features

- **Web Crawling**: Automatically crawls documentation websites to index pages
- **HTML to Markdown**: Converts HTML documentation to readable markdown format
- **MCP Integration**: Works with AI assistants that support the Model Context Protocol
- **Local Storage**: Stores indexed documentation locally for offline access

## Requirements

- Python 3.13+
- Dependencies:
  - beautifulsoup4
  - html2text
  - mcp[cli]
  - requests
