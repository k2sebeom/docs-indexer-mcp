from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Page(BaseModel):
    title: str
    url: str


class Documentation(BaseModel):
    name: str
    base_url: str
    prefix: str
    pages: List[Page] = Field(default_factory=list)
    last_synced: str = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "base_url": self.base_url,
            "prefix": self.prefix,
            "pages": [{"title": page.title, "url": page.url} for page in self.pages],
            "last_synced": self.last_synced or datetime.now().isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Documentation":
        doc = cls(
            name=data["name"],
            base_url=data["base_url"],
            prefix=data["prefix"],
            last_synced=data.get("last_synced"),
        )
        doc.pages = [
            Page(title=p["title"], url=p["url"]) for p in data.get("pages", [])
        ]
        return doc
