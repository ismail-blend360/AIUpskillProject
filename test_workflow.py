# test_workflow.py
import asyncio
from src.fetchers.hackernews_fetcher import HackerNewsFetcher

async def main():
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch_and_save(limit=10)
    print(f"✅ Done! Fetched and saved {len(articles)} articles")

asyncio.run(main())