"""Article data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """
    Represents a news article.

    Using dataclass for automatic __init__, __repr__, etc.
    """

    title: str
    url: str
    published_at: datetime
    source: str
    summary: str = ""
    score: int = 0

    def __post_init__(self):
        """Validate after initialization."""
        if not self.title:
            raise ValueError("Article must have a title")
        if not self.url:
            raise ValueError("Article must have a URL")

    def to_markdown(self) -> str:
        """Convert article to markdown format."""
        return f"""## {self.title}

**Source:** {self.source}  
**URL:** {self.url}  
**Published:** {self.published_at.strftime('%Y-%m-%d %H:%M')}  
**Score:** {self.score}

{self.summary}
"""


# Quick test
if __name__ == "__main__":
    article = Article(
        title="Test Article",
        url="https://example.com",
        published_at=datetime.now(),
        source="test",
    )
    print(article.to_markdown())
    print("✅ Article model works!")
