# tests/test_orchestrator.py

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from src.models.article import Article
from src.orchestrator import FetchOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_with_mocks():
    """
    Test orchestrator with mocked dependencies.

    DIP makes this easy - just inject mocks!
    """
    # Create mock fetcher
    mock_fetcher = Mock()
    mock_fetcher.fetch_and_save = AsyncMock(
        return_value=[
            Article(
                title="Test",
                url="http://test.com",
                published_at=datetime.now(),
                source="test",
                summary="Test",
            )
        ]
    )

    # Create mock storage
    mock_storage = Mock()

    # Create mock transformer
    mock_transformer = Mock()

    # Inject mocks into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=[mock_fetcher], storage=mock_storage, transformer=mock_transformer
    )

    # Test
    articles = await orchestrator.fetch_all()

    # Verify
    assert len(articles) == 1
    assert articles[0].title == "Test"
    assert mock_fetcher.fetch_and_save.called


@pytest.mark.asyncio
async def test_multiple_fetchers():
    """Test with multiple mock fetchers."""
    mock_fetcher1 = Mock()
    mock_fetcher1.fetch_and_save = AsyncMock(
        return_value=[
            Article(
                title="Article 1",
                url="http://1.com",
                published_at=datetime.now(),
                source="test",
                summary="Test",
            )
        ]
    )

    mock_fetcher2 = Mock()
    mock_fetcher2.fetch_and_save = AsyncMock(
        return_value=[
            Article(
                title="Article 2",
                url="http://2.com",
                published_at=datetime.now(),
                source="test",
                summary="Test",
            )
        ]
    )

    orchestrator = FetchOrchestrator(
        fetchers=[mock_fetcher1, mock_fetcher2], storage=Mock(), transformer=Mock()
    )

    articles = await orchestrator.fetch_all()

    assert len(articles) == 2
    print("✅ Multiple fetchers work!")
