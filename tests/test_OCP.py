# Quick test
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer


async def test_github():
    transformer = ArticleTransformer()
    storage = MarkdownStorage()

    fetcher = GitHubTrendingFetcher(transformer, storage)
    articles = await fetcher.fetch_and_save()

    print(f"✅ Fetched {len(articles)} trending repos!")
    print(f"First: {articles[0].title}")


# Run it
import asyncio

asyncio.run(test_github())
