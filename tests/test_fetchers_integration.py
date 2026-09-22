# tests/test_fetchers_integration.py
import pytest

from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher


@pytest.mark.asyncio
async def test_both_fetchers():
    """Test both fetchers work."""
    # HackerNews
    hn = HackerNewsFetcher()
    hn_articles = await hn.fetch(limit=5)
    assert len(hn_articles) > 0

    # RSS
    rss = RSSFetcher("https://hnrss.org/frontpage")
    rss_articles = await rss.fetch()
    assert len(rss_articles) > 0

    print(f"✅ HN: {len(hn_articles)} articles")
    print(f"✅ RSS: {len(rss_articles)} articles")


@pytest.mark.asyncio
async def test_concurrent_fetching():
    """Test fetching from both sources concurrently."""
    import asyncio
    import time

    hn = HackerNewsFetcher()
    rss = RSSFetcher("https://hnrss.org/frontpage")

    start = time.time()

    # Fetch both at same time!
    hn_articles, rss_articles = await asyncio.gather(hn.fetch(limit=5), rss.fetch())

    elapsed = time.time() - start

    total = len(hn_articles) + len(rss_articles)
    print(f"⚡ Fetched {total} articles in {elapsed:.2f}s")

    assert elapsed < 10.0  # Should be fast with concurrent
