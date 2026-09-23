"""Storage interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from src.models.article import Article


class ArticleStorage(ABC):
    """
    Abstract interface for article storage.

    Allows different storage implementations without changing fetchers.
    """

    @abstractmethod
    def save(self, articles: List[Article], filename: str = None) -> Path:
        """
        Save articles to storage.

        Args:
            articles: Articles to save
            filename: Optional filename

        Returns:
            Path or identifier where articles were saved
        """
        pass
