"""Fetch from GitHub Trending."""
from src.fetchers.base_fetcher import BaseFetcher
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from src.models.article import Article


class GitHubTrendingFetcher(BaseFetcher):
    """
    Fetch trending repositories from GitHub.

    NEW fetcher - demonstrates Open/Closed Principle.
    Added WITHOUT modifying any existing code!
    """

    async def fetch_articles(self) -> List[Article]:
        """Scrape GitHub trending page."""
        url = "https://github.com/trending"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')
        repos = soup.select('article.Box-row')

        articles = []
        for repo in repos[:20]:  # Top 20
            # Extract repo info
            title_elem = repo.select_one('h2 a')
            if not title_elem:
                continue

            title = title_elem.text.strip().replace('\n', '').replace(' ', '')
            href = title_elem['href']
            url = f"https://github.com{href}"

            description_elem = repo.select_one('p')
            description = description_elem.text.strip() if description_elem else ''

            stars_elem = repo.select_one('span.d-inline-block.float-sm-right')
            stars = stars_elem.text.strip() if stars_elem else '0'

            article = Article(
                title=title,
                url=url,
                published_at=datetime.now(),
                source='github_trending',
                summary=f"{description} (⭐ {stars})",
                score=0
            )
            articles.append(article)

        return articles

    def get_source_name(self) -> str:
        """Return source name."""
        return "github_trending"