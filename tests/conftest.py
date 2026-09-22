"""Shared pytest fixtures.

This file is automatically loaded by pytest. Add fixtures here as you build
out test coverage milestone by milestone (e.g. a `tmp_articles_dir` fixture
in M1, an `llm_response` fixture in M3, a `mcp_client` fixture in M4).
"""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_article_kwargs() -> dict:
    """Minimal kwargs for constructing an Article in tests.

    You'll define the Article dataclass in Milestone 1. Once it exists,
    tests can use this fixture to build instances without repeating boilerplate.
    """
    from datetime import datetime

    return {
        "title": "Sample article for tests",
        "url": "https://example.com/sample",
        "published_at": datetime(2026, 1, 1, 12, 0, 0),
        "source": "test",
    }
