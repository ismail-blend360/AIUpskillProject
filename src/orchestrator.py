"""Orchestrate multiple news fetchers."""

import asyncio
from typing import List

from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer

class FetchOrchestrator:
    """
    Orchestrates fetching from multiple sources.

    Coordinates HackerNews, RSS, and other fetchers.
    """

    def __init__(
                self,
                fetchers: List[BaseFetcher],
                storage: MarkdownStorage,
                transformer: ArticleTransformer
        ):
        """
        Initialize with injected dependencies.

        Args:
            fetchers: List of fetcher instances
            storage: Storage implementation
            transformer: Transformer instance
        """
        self.fetchers = fetchers
        self.storage = storage
        self.transformer = transformer
    
    async def fetch_all(self) -> List[Article]:
        """Fetch from all sources."""
        all_articles = []

        for fetcher in self.fetchers:
            articles = await fetcher.fetch_and_save()
            all_articles.extend(articles)

        return all_articles
