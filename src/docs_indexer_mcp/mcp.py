from typing import Any, List
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from docs_indexer_mcp.document_manager import DocumentManager
from docs_indexer_mcp.models import Page

# Initialize FastMCP server
mcp = FastMCP("docs-indexer")


@mcp.tool()
async def list_documentations(
    ctx: Context,
) -> list[Any]:
    """
    List all documentations.
    """

    docs = DocumentManager.list_docs()
    return docs


@mcp.tool()
async def list_pages(
    ctx: Context,
    doc_name: str = Field(description="Name of the documentation to list pages"),
) -> List[Page]:
    """
    List available pages in a documentation.
    """
    doc = DocumentManager.load_documentation(doc_name)
    return doc.pages


@mcp.tool()
async def read_page(
    ctx: Context,
    doc_name: str = Field(description="Name of the documentation to read"),
    url: str = Field(description="Url of the page to read"),
) -> str:
    """
    Read a specific page from documentation.
    """
    title, content = DocumentManager.read_page(doc_name, url)
    return f"# {title}\n" + content



def main():
    mcp.run()
