"""Transform raw data to Article objects."""

from datetime import datetime
from typing import Any, Dict, List

from src.models.article import Article


class ArticleTransformer:
    """
    Transforms raw data from various sources to Article objects.

    Single Responsibility: Data transformation only.
    """

    def transform_hackernews(self, raw_data: List[Dict]) -> List[Article]:
        """
        Transform HackerNews API response to Articles.

        Args:
            raw_data: List of HN items from API

        Returns:
            List of Article objects
        """
        articles = []

        for item in raw_data:
            if not item.get("url"):
                continue

            article = Article(
                title=item.get("title", ""),
                url=item["url"],
                published_at=datetime.fromtimestamp(item.get("time", 0)),
                source="hackernews",
                summary=item.get("text", "")[:200] if item.get("text") else "",
                score=item.get("score", 0),
            )
            articles.append(article)

        return articles

    def transform_rss(self, entries: List[Any]) -> List[Article]:
        """
        Transform RSS feed entries to Articles.

        Args:
            entries: List of RSS entries from feedparser

        Returns:
            List of Article objects
        """
        articles = []

        for entry in entries:
            article = Article(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                published_at=self._parse_date(entry.get("published")),
                source="rss",
                summary=entry.get("summary", "")[:200],
            )
            articles.append(article)

        return articles

    def _parse_date(self, date_str: str) -> datetime:
        """Parse various date formats."""
        # Date parsing logic here
        # You can copy from your existing code
        try:
            from dateutil import parser

            return parser.parse(date_str)
        except:
            return datetime.now()
