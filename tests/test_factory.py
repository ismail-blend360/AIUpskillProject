import asyncio
import pytest

from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage
from src.factories.fetcher_factory import FetcherFactory
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.strategies.rate_limit_strategy import SemaphoreStrategy


def test_factory():
    """Test factory pattern."""
    transformer = ArticleTransformer()
    storage = MarkdownStorage()

    # Create via factory
    fetcher = FetcherFactory.create('hackernews', transformer, storage)

    assert isinstance(fetcher, HackerNewsFetcher)
    assert fetcher.get_source_name() == 'hackernews'

    # List available types
    types = FetcherFactory.get_available_types()
    assert 'hackernews' in types
    assert 'github' in types

    print("✅ Factory works!")

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting strategies."""
    import time

    # Semaphore - allows 2 concurrent
    sem_strategy = SemaphoreStrategy(2)

    async def task():
        await sem_strategy.acquire()
        await asyncio.sleep(0.1)
        sem_strategy.release()

    start = time.time()
    await asyncio.gather(*[task() for _ in range(4)])
    elapsed = time.time() - start

    # Should take ~0.2s (2 at a time, 0.1s each)
    assert elapsed >= 0.2
    assert elapsed < 0.3

    print("✅ Rate limiting works!")