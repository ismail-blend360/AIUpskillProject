# src/fetchers/rss_fetcher.py

from typing import List

import feedparser

from src.fetchers.base_fetcher import BaseFetcher
from src.models.article import Article


class RSSFetcher(BaseFetcher):
    """Fetch from RSS feed."""

    def __init__(self, feed_url: str, transformer, storage):
        super().__init__(transformer, storage)
        self.feed_url = feed_url

    async def fetch_articles(self) -> List[Article]:
        """Fetch from RSS feed."""
        feed = feedparser.parse(self.feed_url)
        return self.transformer.transform_rss(feed.entries)

    def get_source_name(self) -> str:
        """Return source name."""
        return "rss"


# """Fetch articles from RSS feeds."""

# import asyncio
# from datetime import datetime
# from typing import List

# import feedparser
# from dateutil import parser as date_parser

# from src.models.article import Article
# from src.storage.markdown_storage import MarkdownStorage


# class RSSFetcher:
#     """
#     Fetches articles from RSS feeds.

#     Uses feedparser library for RSS parsing.
#     """

#     def __init__(self, feed_url: str):
#         """
#         Initialize RSS fetcher.

#         Args:
#             feed_url: URL of RSS feed
#         """
#         self.feed_url = feed_url
#         self.storage = MarkdownStorage()

#     async def fetch(self) -> List[Article]:
#         """
#         Fetch articles from RSS feed.

#         Returns:
#             List of Article objects
#         """
#         print(f"📰 Fetching from RSS: {self.feed_url}")

#         # feedparser is sync, run in executor
#         loop = asyncio.get_event_loop()
#         feed = await loop.run_in_executor(
#             None, feedparser.parse, self.feed_url  # Default executor
#         )

#         # Parse entries
#         articles = []
#         for entry in feed.entries:
#             article = self._parse_entry(entry)
#             if article:
#                 articles.append(article)

#         print(f"✅ Fetched {len(articles)} RSS articles")
#         return articles

#     def _parse_entry(self, entry) -> Article:
#         """Parse RSS entry to Article."""
#         try:
#             # Get title
#             title = entry.get("title", "No Title")

#             # Get URL
#             url = entry.get("link", "")
#             if not url:
#                 return None

#             # Parse date
#             published_str = entry.get("published", entry.get("updated", ""))
#             if published_str:
#                 try:
#                     published_at = date_parser.parse(published_str)
#                 except:
#                     published_at = datetime.now()
#             else:
#                 published_at = datetime.now()

#             # Get summary
#             summary = entry.get("summary", entry.get("description", ""))
#             # Clean HTML tags (basic)
#             import re

#             summary = re.sub("<.*?>", "", summary)[:200]

#             return Article(
#                 title=title,
#                 url=url,
#                 published_at=published_at,
#                 source="rss",
#                 summary=summary,
#             )
#         except Exception as e:
#             print(f"⚠️  Failed to parse entry: {e}")
#             return None

#     async def fetch_and_save(self) -> List[Article]:
#         """Fetch and save articles."""
#         articles = await self.fetch()

#         if articles:
#             # Extract feed name from URL
#             feed_name = self.feed_url.split("//")[-1].split("/")[0]
#             filename = f"rss_{feed_name}_articles.md"
#             self.storage.save(articles, filename)

#         return articles


# # Test it
# async def test_rss():
#     """Test RSS fetcher."""
#     # HackerNews RSS feed
#     fetcher = RSSFetcher("https://hnrss.org/frontpage")
#     articles = await fetcher.fetch_and_save()

#     print(f"\n📊 Fetched {len(articles)} articles")
#     for article in articles[:3]:
#         print(f"  - {article.title[:50]}...")


# if __name__ == "__main__":
#     asyncio.run(test_rss())
