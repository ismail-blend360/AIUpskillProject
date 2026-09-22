"""Base fetcher interface."""
from abc import ABC, abstractmethod
from typing import List
from src.models.article import Article


class BaseFetcher(ABC):
    """
    Abstract base class for all article fetchers.

    Defines the contract that all fetchers must follow.
    Enables Open/Closed Principle.
    """

    def __init__(self, transformer, storage):
        """
        Initialize fetcher with dependencies.

        Args:
            transformer: ArticleTransformer instance
            storage: MarkdownStorage instance
        """
        self.transformer = transformer
        self.storage = storage

    @abstractmethod
    async def fetch_articles(self) -> List[Article]:
        """
        Fetch articles from source.

        Must be implemented by subclasses.
        This is the ONLY method that varies by source.

        Returns:
            List of Article objects
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of this source.

        Returns:
            Source name (e.g., 'hackernews', 'rss', 'github')
        """
        pass

    # Common methods (same for all fetchers)

    async def fetch_and_save(self) -> List[Article]:
        """
        Fetch articles and save to storage.

        Template method - same for all fetchers.
        """
        articles = await self.fetch_articles()

        if articles:
            filename = f"{self.get_source_name()}_articles.md"
            self.storage.save(articles, filename)

        return articles