"""Main entry point for news fetcher."""

import asyncio
import sys

from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage
from src.factories.fetcher_factory import FetcherFactory

async def main():
    """Main entry point with dependency injection."""

    # Create dependencies
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")

    config_sources = ['hackernews', 'github']
    fetchers = [
        FetcherFactory.create(source, transformer, storage)
        for source in config_sources
    ]

    # Inject dependencies into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=fetchers,
        storage=storage,
        transformer=transformer
    )

    # Run
    articles = await orchestrator.fetch_all()
    print(f"✅ Fetched {len(articles)} articles total")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
