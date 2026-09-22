# src/fetchers/interfaces.py

from abc import ABC, abstractmethod


class AuthenticatedFetcher(ABC):
    """Interface for fetchers that require authentication."""

    @abstractmethod
    async def authenticate(self) -> bool:
        """
        Authenticate with the source.

        Returns:
            True if authentication successful
        """
        pass


class PaginatedFetcher(ABC):
    """Interface for fetchers that support pagination."""

    @abstractmethod
    async def fetch_page(self, page: int) -> List[Article]:
        """
        Fetch specific page of results.

        Args:
            page: Page number (1-indexed)

        Returns:
            Articles from that page
        """
        pass