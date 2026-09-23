"""Test Liskov Substitution Principle."""

import pytest

from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer


@pytest.mark.asyncio
async def test_all_fetchers_substitutable():
    """
    Test that all fetchers can be used interchangeably.

    This proves Liskov Substitution Principle.
    """
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/test")

    # Create all fetchers
    fetchers = [
        HackerNewsFetcher(transformer, storage),
        RSSFetcher("https://hnrss.org/frontpage", transformer, storage),
        GitHubTrendingFetcher(transformer, storage),
    ]

    # Each fetcher should work identically
    for fetcher in fetchers:
        # Should have same interface
        assert hasattr(fetcher, "fetch_articles")
        assert hasattr(fetcher, "get_source_name")
        assert hasattr(fetcher, "fetch_and_save")

        # Should return List[Article]
        articles = await fetcher.fetch_articles()
        assert isinstance(articles, list)

        # All articles should have same structure
        if articles:
            article = articles[0]
            assert hasattr(article, "title")
            assert hasattr(article, "url")
            assert hasattr(article, "source")

        # Should have source name
        source = fetcher.get_source_name()
        assert isinstance(source, str)
        assert len(source) > 0

    print("✅ All fetchers are substitutable!")


@pytest.mark.asyncio
async def test_polymorphic_usage():
    """Test using fetchers polymorphically."""
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/test")

    def process_fetcher(fetcher: BaseFetcher):
        """This function accepts ANY fetcher."""
        # Should work with all fetchers
        source = fetcher.get_source_name()
        return source

    # All fetchers work with same function!
    hn = HackerNewsFetcher(transformer, storage)
    assert process_fetcher(hn) == "hackernews"

    gh = GitHubTrendingFetcher(transformer, storage)
    assert process_fetcher(gh) == "github_trending"

    print("✅ Polymorphism works!")
