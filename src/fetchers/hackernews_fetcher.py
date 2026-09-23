# src/fetchers/hackernews_fetcher.py

from typing import List

import aiohttp

from src.fetchers.base_fetcher import BaseFetcher
from src.models.article import Article
from src.strategies.rate_limit_strategy import SemaphoreStrategy


class HackerNewsFetcher(BaseFetcher):
    """
    Fetch top stories from HackerNews.

    Inherits from BaseFetcher.
    Only implements source-specific logic.
    """

    def __init__(self, transformer, storage, rate_limiter=None):
        super().__init__(transformer, storage)
        # Use provided strategy or default
        self.rate_limiter = rate_limiter or SemaphoreStrategy(10)

    async def fetch_articles(self) -> List[Article]:
        """Fetch from HackerNews API."""
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"

        await self.rate_limiter.acquire()
        try:
            async with aiohttp.ClientSession() as session:
                # Get top story IDs
                async with session.get(url) as response:
                    story_ids = await response.json()

                # Fetch first 30 stories
                stories = []
                for story_id in story_ids[:30]:
                    item_url = (
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    )
                    async with session.get(item_url) as response:
                        item = await response.json()
                        if item:
                            stories.append(item)
        finally:
            self.rate_limiter.release()
            # Transform using injected transformer
        return self.transformer.transform_hackernews(stories)

    def get_source_name(self) -> str:
        """Return source name."""
        return "hackernews"


# """Fetch top stories from HackerNews."""
# import asyncio
# import aiohttp
# from typing import List
# from datetime import datetime
# from src.models.article import Article
# from src.storage.markdown_storage import MarkdownStorage
# from src.utils.rate_limiter import RateLimiter

# class HackerNewsFetcher:
#     """
#     Fetches top stories from HackerNews API.

#     API Docs: https://github.com/HackerNews/API
#     """

#     BASE_URL = "https://hacker-news.firebaseio.com/v0"

#     async def fetch(self, limit: int = 30) -> List[Article]:
#         """
#         Fetch top stories from HackerNews.

#         Args:
#             limit: Number of stories to fetch (default 30)

#         Returns:
#             List of Article objects
#         """
#         print(f"📰 Fetching {limit} stories from HackerNews...")

#         # Step 1: Get top story IDs
#         story_ids = await self._fetch_top_story_ids()

#         # Step 2: Fetch first N stories concurrently
#         articles = await self._fetch_stories(story_ids[:limit])

#         print(f"✅ Fetched {len(articles)} HackerNews stories")
#         return articles

#     async def _fetch_top_story_ids(self) -> List[int]:
#         """Fetch list of top story IDs."""
#         url = f"{self.BASE_URL}/topstories.json"

#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 story_ids = await response.json()
#                 return story_ids

#     async def _fetch_stories(self, story_ids: List[int]) -> List[Article]:
#         """
#         Fetch multiple stories concurrently.

#         This is where async shines - fetch all at once!
#         """
#         # Create tasks for all stories
#         tasks = [self._fetch_story(story_id) for story_id in story_ids]

#         # Run all tasks concurrently
#         stories = await asyncio.gather(*tasks)

#         # Filter out None (failed fetches)
#         return [s for s in stories if s is not None]

#     # async def _fetch_story(self, story_id: int) -> Article:
#     #     """Fetch single story by ID."""
#     #     url = f"{self.BASE_URL}/item/{story_id}.json"

#     #     try:
#     #         async with aiohttp.ClientSession() as session:
#     #             async with session.get(url) as response:
#     #                 data = await response.json()

#     #                 # Skip if no URL (Ask HN, etc.)
#     #                 if not data.get('url'):
#     #                     return None

#     #                 # Convert to Article
#     #                 return Article(
#     #                     title=data.get('title', 'No Title'),
#     #                     url=data['url'],
#     #                     published_at=datetime.fromtimestamp(
#     #                         data.get('time', 0)
#     #                     ),
#     #                     source='hackernews',
#     #                     summary=data.get('text', '')[:200],  # First 200 chars
#     #                     score=data.get('score', 0)
#     #                 )
#     #     except Exception as e:
#     #         print(f"⚠️  Failed to fetch story {story_id}: {e}")
#     #         return None

#     async def fetch_and_save(self, limit: int = 30) -> List[Article]:
#         """Fetch articles and save to markdown."""
#         articles = await self.fetch(limit)

#         if articles:
#             self.storage.save(articles, "hackernews_articles.md")

#         return articles

#     def __init__(self, transformer=None, storage=None):
#         self.transformer = transformer
#         self.storage = storage or MarkdownStorage()
#         self.rate_limiter = RateLimiter(max_concurrent=10)

#     async def _fetch_story(self, story_id: int) -> Article:
#         """Fetch single story with rate limiting."""
#         url = f"{self.BASE_URL}/item/{story_id}.json"

#         try:
#             # Use rate limiter
#             async with self.rate_limiter:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(url) as response:
#                         data = await response.json()
#                         # Skip if no URL (Ask HN, etc.)
#                         if not data.get('url'):
#                             return None

#                         # Convert to Article
#                         return Article(
#                             title=data.get('title', 'No Title'),
#                             url=data['url'],
#                             published_at=datetime.fromtimestamp(
#                                 data.get('time', 0)
#                             ),
#                             source='hackernews',
#                             summary=data.get('text', '')[:200],  # First 200 chars
#                             score=data.get('score', 0)
#                         )
#         except Exception as e:
#             print(f"⚠️  Failed to fetch story {story_id}: {e}")
#             return None

# # Test it
# async def test_fetch():
#     """Quick test of fetcher."""
#     fetcher = HackerNewsFetcher()
#     articles = await fetcher.fetch(limit=5)

#     print(f"\n📊 Results:")
#     for article in articles:
#         print(f"  - {article.title[:50]}...")

#     return articles


# if __name__ == "__main__":
#     asyncio.run(test_fetch())
