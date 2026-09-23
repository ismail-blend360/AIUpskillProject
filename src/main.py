"""Main entry point for news fetcher."""

import asyncio

from src.factories.fetcher_factory import FetcherFactory
from src.orchestrator import FetchOrchestrator
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer


async def main():
    """Main entry point with dependency injection."""

    # Create dependencies
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")

    config_sources = ["hackernews", "github"]
    fetchers = [
        FetcherFactory.create(source, transformer, storage) for source in config_sources
    ]

    # Inject dependencies into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=fetchers, storage=storage, transformer=transformer
    )

    # Run
    articles = await orchestrator.fetch_all()
    print(f"✅ Fetched {len(articles)} articles total")


if __name__ == "__main__":
    asyncio.run(main())
