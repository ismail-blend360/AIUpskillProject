# Milestone 1: Async News Fetcher

**⏰ Time Commitment:** 3-4 evenings (6-8 hours)  
**When:** Week 1, Days 2-5  
**Prerequisites:** Milestone 0 complete  
**Checkpoint:** ✓ Checkpoint 1 (after completion)  
**Next Milestone:** [Milestone 2: SOLID Refactoring](milestone-2-solid-refactoring.md)

---

## 🎯 Learning Objectives

By the end of this week, you will:
- Understand async/await fundamentals
- Make async HTTP requests with aiohttp
- Parse RSS feeds
- Implement basic rate limiting
- Save data to markdown files
- Write async tests with pytest
- Build your first production-ready component

**This is your first REAL coding!** 🚀

---

## 📚 Week 1 Overview

```
Week 1: Async Foundations
├── Day 1 (Evening 1): Milestone 0 - Setup ✅ Done
├── Day 2 (Evening 2): Async Basics + HackerNews Fetcher
├── Day 3 (Evening 3): RSS Fetcher + Rate Limiting
├── Day 4 (Evening 4): Orchestrator + Tests
└── Day 5 (Evening 5): Polish + PR (optional)

Total: 6-8 hours over 3-4 evenings
```

---

## 📖 Required Reading (Before Evening 2)

**Read these first (30 minutes total):**

1. **Async/Await Basics (15 min)**
   - https://realpython.com/async-io-python/
   - Sections: "The asyncio Package and async/await" and "Async IO Design Patterns"

2. **aiohttp Quick Start (10 min)**
   - https://docs.aiohttp.org/en/stable/client_quickstart.html
   - Just the "Make a Request" section

3. **RSS Overview (5 min)**
   - https://www.markdownguide.org/basic-syntax/
   - Just skim, you'll use feedparser library

**Done reading?** Start Evening 2! 🚀

---

## 🌙 Evening 2: Async Basics + HackerNews Fetcher

**⏰ Time:** 1.5-2 hours  
**Goal:** Build your first async fetcher

### **Timeline:**

```
7:30 PM - Start
├── 7:30-7:50 PM (20 min) - Understand async basics
├── 7:50-8:30 PM (40 min) - Build HackerNews fetcher
├── 8:30-9:00 PM (30 min) - Save to markdown
└── 9:00-9:20 PM (20 min) - Basic tests
9:20 PM - Done!
```

---

### **Step 1: Understand Async Basics (20 min)**

**Read this code and understand it:**

```python
# Regular synchronous code (slow!)
def fetch_url(url):
    response = requests.get(url)  # Blocks here!
    return response.json()

# Takes 6 seconds for 3 URLs
for url in urls:
    data = fetch_url(url)  # Wait 2 seconds each

# Async code (fast!)
async def fetch_url_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()  # Doesn't block!

# Takes 2 seconds for 3 URLs (concurrent!)
tasks = [fetch_url_async(url) for url in urls]
results = await asyncio.gather(*tasks)  # Run all at once!
```

**Key concepts:**
- `async def` = function can use `await`
- `await` = pause here, let others run
- `asyncio.gather()` = run multiple tasks concurrently

**Create test file to practice:**

```python
# practice_async.py
import asyncio
import aiohttp

async def fetch_example():
    """Practice async HTTP."""
    url = "https://api.github.com/repos/python/cpython"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(f"✅ Fetched: {data['name']}")
            return data

# Run it
asyncio.run(fetch_example())
```

**Try it:**

```bash
python practice_async.py

# Should print: ✅ Fetched: cpython
```

**Understand it?** Move on!

---

### **Step 2: Create Article Model (15 min)**

**Create:** `src/models/article.py`

```python
"""Article data model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """
    Represents a news article.
    
    Using dataclass for automatic __init__, __repr__, etc.
    """
    
    title: str
    url: str
    published_at: datetime
    source: str
    summary: str = ""
    score: int = 0
    
    def __post_init__(self):
        """Validate after initialization."""
        if not self.title:
            raise ValueError("Article must have a title")
        if not self.url:
            raise ValueError("Article must have a URL")
    
    def to_markdown(self) -> str:
        """Convert article to markdown format."""
        return f"""## {self.title}

**Source:** {self.source}  
**URL:** {self.url}  
**Published:** {self.published_at.strftime('%Y-%m-%d %H:%M')}  
**Score:** {self.score}

{self.summary}
"""


# Quick test
if __name__ == "__main__":
    article = Article(
        title="Test Article",
        url="https://example.com",
        published_at=datetime.now(),
        source="test"
    )
    print(article.to_markdown())
    print("✅ Article model works!")
```

**Test it:**

```bash
python src/models/article.py

# Should show formatted markdown
```

---

### **Step 3: Build HackerNews Fetcher (40 min)**

**Create:** `src/fetchers/hackernews_fetcher.py`

```python
"""Fetch top stories from HackerNews."""
import asyncio
import aiohttp
from typing import List
from datetime import datetime
from src.models.article import Article


class HackerNewsFetcher:
    """
    Fetches top stories from HackerNews API.
    
    API Docs: https://github.com/HackerNews/API
    """
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    async def fetch(self, limit: int = 30) -> List[Article]:
        """
        Fetch top stories from HackerNews.
        
        Args:
            limit: Number of stories to fetch (default 30)
            
        Returns:
            List of Article objects
        """
        print(f"📰 Fetching {limit} stories from HackerNews...")
        
        # Step 1: Get top story IDs
        story_ids = await self._fetch_top_story_ids()
        
        # Step 2: Fetch first N stories concurrently
        articles = await self._fetch_stories(story_ids[:limit])
        
        print(f"✅ Fetched {len(articles)} HackerNews stories")
        return articles
    
    async def _fetch_top_story_ids(self) -> List[int]:
        """Fetch list of top story IDs."""
        url = f"{self.BASE_URL}/topstories.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                story_ids = await response.json()
                return story_ids
    
    async def _fetch_stories(self, story_ids: List[int]) -> List[Article]:
        """
        Fetch multiple stories concurrently.
        
        This is where async shines - fetch all at once!
        """
        # Create tasks for all stories
        tasks = [self._fetch_story(story_id) for story_id in story_ids]
        
        # Run all tasks concurrently
        stories = await asyncio.gather(*tasks)
        
        # Filter out None (failed fetches)
        return [s for s in stories if s is not None]
    
    async def _fetch_story(self, story_id: int) -> Article:
        """Fetch single story by ID."""
        url = f"{self.BASE_URL}/item/{story_id}.json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    
                    # Skip if no URL (Ask HN, etc.)
                    if not data.get('url'):
                        return None
                    
                    # Convert to Article
                    return Article(
                        title=data.get('title', 'No Title'),
                        url=data['url'],
                        published_at=datetime.fromtimestamp(
                            data.get('time', 0)
                        ),
                        source='hackernews',
                        summary=data.get('text', '')[:200],  # First 200 chars
                        score=data.get('score', 0)
                    )
        except Exception as e:
            print(f"⚠️  Failed to fetch story {story_id}: {e}")
            return None


# Test it
async def test_fetch():
    """Quick test of fetcher."""
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch(limit=5)
    
    print(f"\n📊 Results:")
    for article in articles:
        print(f"  - {article.title[:50]}...")
    
    return articles


if __name__ == "__main__":
    asyncio.run(test_fetch())
```

**Test your fetcher:**

```bash
python src/fetchers/hackernews_fetcher.py

# Should fetch and print 5 articles!
# Takes ~2 seconds (concurrent fetch)
```

**Working?** Great! Move on.

---

### **Step 4: Save to Markdown (30 min)**

**Create:** `src/storage/markdown_storage.py`

```python
"""Save articles to markdown files."""
from pathlib import Path
from typing import List
from datetime import datetime
from src.models.article import Article


class MarkdownStorage:
    """
    Saves articles to markdown files.
    
    Creates files in data/articles/ directory.
    """
    
    def __init__(self, base_path: str = "data/articles"):
        """
        Initialize storage.
        
        Args:
            base_path: Directory to save articles
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, articles: List[Article], filename: str = None) -> Path:
        """
        Save articles to markdown file.
        
        Args:
            articles: List of articles to save
            filename: Optional filename, auto-generated if not provided
            
        Returns:
            Path to saved file
        """
        if filename is None:
            # Auto-generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"articles_{timestamp}.md"
        
        filepath = self.base_path / filename
        
        # Write articles to file
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# News Articles\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Articles:** {len(articles)}\n\n")
            f.write("---\n\n")
            
            # Articles
            for article in articles:
                f.write(article.to_markdown())
                f.write("\n---\n\n")
        
        print(f"💾 Saved {len(articles)} articles to: {filepath}")
        return filepath


# Test it
if __name__ == "__main__":
    from src.models.article import Article
    
    # Create test article
    test_article = Article(
        title="Test Article",
        url="https://example.com",
        published_at=datetime.now(),
        source="test",
        summary="This is a test article."
    )
    
    # Save it
    storage = MarkdownStorage()
    path = storage.save([test_article], "test.md")
    
    # Verify
    assert path.exists()
    print(f"✅ Saved to: {path}")
    print(f"✅ File contents:")
    print(path.read_text()[:200])
```

**Test it:**

```bash
python src/storage/markdown_storage.py

# Should create file in data/articles/test.md
# Check the file!
cat data/articles/test.md
```

---

### **Step 5: Put It Together (15 min)**

**Update your fetcher to save:**

```python
# Add to HackerNewsFetcher
from src.storage.markdown_storage import MarkdownStorage

class HackerNewsFetcher:
    def __init__(self):
        self.storage = MarkdownStorage()
    
    async def fetch_and_save(self, limit: int = 30) -> List[Article]:
        """Fetch articles and save to markdown."""
        articles = await self.fetch(limit)
        
        if articles:
            self.storage.save(articles, "hackernews_articles.md")
        
        return articles
```

**Test full workflow:**

```python
# test_workflow.py
import asyncio
from src.fetchers.hackernews_fetcher import HackerNewsFetcher

async def main():
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch_and_save(limit=10)
    print(f"✅ Done! Fetched and saved {len(articles)} articles")

asyncio.run(main())
```

```bash
python test_workflow.py

# Check your file!
cat data/articles/hackernews_articles.md
```

---

### **Step 6: Basic Tests (20 min)**

**Create:** `tests/test_hackernews_fetcher.py`

```python
"""Tests for HackerNews fetcher."""
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.models.article import Article


@pytest.mark.asyncio
async def test_fetch_returns_articles():
    """Test that fetch returns list of articles."""
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch(limit=5)
    
    # Should get some articles
    assert len(articles) > 0
    assert len(articles) <= 5
    
    # Each should be an Article
    for article in articles:
        assert isinstance(article, Article)
        assert article.title
        assert article.url
        assert article.source == 'hackernews'


@pytest.mark.asyncio
async def test_fetch_concurrent():
    """Test that fetch is fast (concurrent)."""
    import time
    
    fetcher = HackerNewsFetcher()
    
    start = time.time()
    articles = await fetcher.fetch(limit=10)
    elapsed = time.time() - start
    
    # Should be faster than sequential (< 5 seconds)
    assert elapsed < 5.0
    assert len(articles) > 0
    
    print(f"⚡ Fetched {len(articles)} articles in {elapsed:.2f}s")
```

**Run tests:**

```bash
pytest tests/test_hackernews_fetcher.py -v

# Should pass! ✅
```

---

### **Evening 2 Deliverable:**

✅ HackerNews fetcher working  
✅ Async concurrent fetching  
✅ Articles saved to markdown  
✅ Basic tests passing  
✅ First real code complete!  

**Time used:** 1.5-2 hours

---

## 🌙 Evening 3: RSS Fetcher + Rate Limiting

**⏰ Time:** 1.5-2 hours  
**Goal:** Add RSS source and rate limiting

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:15 PM (45 min) - Build RSS fetcher
├── 8:15-8:45 PM (30 min) - Add rate limiting
└── 8:45-9:15 PM (30 min) - Test everything
9:15 PM - Done!
```

---

### **Step 1: Install Dependencies (5 min)**

```bash
# Add to requirements.txt if not there
pip install feedparser

# Or install directly
pip install feedparser
```

---

### **Step 2: Build RSS Fetcher (40 min)**

**Create:** `src/fetchers/rss_fetcher.py`

```python
"""Fetch articles from RSS feeds."""
import asyncio
import feedparser
from typing import List
from datetime import datetime
from dateutil import parser as date_parser
from src.models.article import Article
from src.storage.markdown_storage import MarkdownStorage


class RSSFetcher:
    """
    Fetches articles from RSS feeds.
    
    Uses feedparser library for RSS parsing.
    """
    
    def __init__(self, feed_url: str):
        """
        Initialize RSS fetcher.
        
        Args:
            feed_url: URL of RSS feed
        """
        self.feed_url = feed_url
        self.storage = MarkdownStorage()
    
    async def fetch(self) -> List[Article]:
        """
        Fetch articles from RSS feed.
        
        Returns:
            List of Article objects
        """
        print(f"📰 Fetching from RSS: {self.feed_url}")
        
        # feedparser is sync, run in executor
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(
            None,  # Default executor
            feedparser.parse,
            self.feed_url
        )
        
        # Parse entries
        articles = []
        for entry in feed.entries:
            article = self._parse_entry(entry)
            if article:
                articles.append(article)
        
        print(f"✅ Fetched {len(articles)} RSS articles")
        return articles
    
    def _parse_entry(self, entry) -> Article:
        """Parse RSS entry to Article."""
        try:
            # Get title
            title = entry.get('title', 'No Title')
            
            # Get URL
            url = entry.get('link', '')
            if not url:
                return None
            
            # Parse date
            published_str = entry.get('published', entry.get('updated', ''))
            if published_str:
                try:
                    published_at = date_parser.parse(published_str)
                except:
                    published_at = datetime.now()
            else:
                published_at = datetime.now()
            
            # Get summary
            summary = entry.get('summary', entry.get('description', ''))
            # Clean HTML tags (basic)
            import re
            summary = re.sub('<.*?>', '', summary)[:200]
            
            return Article(
                title=title,
                url=url,
                published_at=published_at,
                source='rss',
                summary=summary
            )
        except Exception as e:
            print(f"⚠️  Failed to parse entry: {e}")
            return None
    
    async def fetch_and_save(self) -> List[Article]:
        """Fetch and save articles."""
        articles = await self.fetch()
        
        if articles:
            # Extract feed name from URL
            feed_name = self.feed_url.split('//')[-1].split('/')[0]
            filename = f"rss_{feed_name}_articles.md"
            self.storage.save(articles, filename)
        
        return articles


# Test it
async def test_rss():
    """Test RSS fetcher."""
    # HackerNews RSS feed
    fetcher = RSSFetcher("https://hnrss.org/frontpage")
    articles = await fetcher.fetch_and_save()
    
    print(f"\n📊 Fetched {len(articles)} articles")
    for article in articles[:3]:
        print(f"  - {article.title[:50]}...")


if __name__ == "__main__":
    asyncio.run(test_rss())
```

**Test it:**

```bash
python src/fetchers/rss_fetcher.py

# Should fetch RSS articles!
```

---

### **Step 3: Add Simple Rate Limiting (30 min)**

**Create:** `src/utils/rate_limiter.py`

```python
"""Simple rate limiting."""
import asyncio
from typing import Optional


class RateLimiter:
    """
    Simple semaphore-based rate limiter.
    
    Limits concurrent operations.
    """
    
    def __init__(self, max_concurrent: int = 10):
        """
        Initialize rate limiter.
        
        Args:
            max_concurrent: Maximum concurrent operations
        """
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def __aenter__(self):
        """Acquire semaphore."""
        await self.semaphore.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release semaphore."""
        self.semaphore.release()
    
    async def execute(self, coro):
        """
        Execute coroutine with rate limiting.
        
        Args:
            coro: Coroutine to execute
            
        Returns:
            Result of coroutine
        """
        async with self:
            return await coro


# Test it
async def test_rate_limiter():
    """Test rate limiter."""
    import time
    
    limiter = RateLimiter(max_concurrent=2)
    
    async def slow_task(n):
        """Simulated slow task."""
        async with limiter:
            print(f"  Task {n} starting")
            await asyncio.sleep(0.5)
            print(f"  Task {n} done")
            return n
    
    print("Testing with max_concurrent=2...")
    start = time.time()
    
    # Run 4 tasks - should take ~1 second (2 at a time)
    results = await asyncio.gather(*[slow_task(i) for i in range(4)])
    
    elapsed = time.time() - start
    print(f"\n✅ Completed in {elapsed:.2f}s")
    print(f"   (Should be ~1.0s with 2 concurrent)")


if __name__ == "__main__":
    asyncio.run(test_rate_limiter())
```

**Test it:**

```bash
python src/utils/rate_limiter.py

# Should show tasks running 2 at a time
```

---

### **Step 4: Add Rate Limiting to Fetcher (15 min)**

**Update HackerNewsFetcher:**

```python
# In hackernews_fetcher.py
from src.utils.rate_limiter import RateLimiter

class HackerNewsFetcher:
    def __init__(self):
        self.storage = MarkdownStorage()
        self.rate_limiter = RateLimiter(max_concurrent=10)
    
    async def _fetch_story(self, story_id: int) -> Article:
        """Fetch single story with rate limiting."""
        url = f"{self.BASE_URL}/item/{story_id}.json"
        
        try:
            # Use rate limiter
            async with self.rate_limiter:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        # ... rest of code
        except Exception as e:
            print(f"⚠️  Failed to fetch story {story_id}: {e}")
            return None
```

---

### **Step 5: Test Both Fetchers (30 min)**

**Create integration test:**

```python
# tests/test_fetchers_integration.py
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher


@pytest.mark.asyncio
async def test_both_fetchers():
    """Test both fetchers work."""
    # HackerNews
    hn = HackerNewsFetcher()
    hn_articles = await hn.fetch(limit=5)
    assert len(hn_articles) > 0
    
    # RSS
    rss = RSSFetcher("https://hnrss.org/frontpage")
    rss_articles = await rss.fetch()
    assert len(rss_articles) > 0
    
    print(f"✅ HN: {len(hn_articles)} articles")
    print(f"✅ RSS: {len(rss_articles)} articles")


@pytest.mark.asyncio
async def test_concurrent_fetching():
    """Test fetching from both sources concurrently."""
    import time
    import asyncio
    
    hn = HackerNewsFetcher()
    rss = RSSFetcher("https://hnrss.org/frontpage")
    
    start = time.time()
    
    # Fetch both at same time!
    hn_articles, rss_articles = await asyncio.gather(
        hn.fetch(limit=5),
        rss.fetch()
    )
    
    elapsed = time.time() - start
    
    total = len(hn_articles) + len(rss_articles)
    print(f"⚡ Fetched {total} articles in {elapsed:.2f}s")
    
    assert elapsed < 10.0  # Should be fast with concurrent
```

**Run tests:**

```bash
pytest tests/test_fetchers_integration.py -v

# Both should pass!
```

---

### **Evening 3 Deliverable:**

✅ RSS fetcher working  
✅ Rate limiting implemented  
✅ Both fetchers tested  
✅ Concurrent fetching working  

**Time used:** 1.5-2 hours

---

## 🌙 Evening 4: Orchestrator + Complete Tests

**⏰ Time:** 1.5-2 hours  
**Goal:** Orchestrate all fetchers and achieve 60%+ test coverage

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:15 PM (45 min) - Build orchestrator
├── 8:15-9:00 PM (45 min) - Write comprehensive tests
└── 9:00-9:15 PM (15 min) - Verify coverage
9:15 PM - Done!
```

---

### **Step 1: Build Orchestrator (45 min)**

**Create:** `src/orchestrator.py`

```python
"""Orchestrate multiple news fetchers."""
import asyncio
from typing import List
from src.models.article import Article
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.storage.markdown_storage import MarkdownStorage


class FetchOrchestrator:
    """
    Orchestrates fetching from multiple sources.
    
    Coordinates HackerNews, RSS, and other fetchers.
    """
    
    def __init__(self):
        """Initialize orchestrator with all fetchers."""
        self.storage = MarkdownStorage()
        self.fetchers = []
        
        # Add fetchers
        self._setup_fetchers()
    
    def _setup_fetchers(self):
        """Setup all news fetchers."""
        # HackerNews
        self.fetchers.append(
            ('HackerNews', HackerNewsFetcher())
        )
        
        # RSS feeds
        rss_feeds = [
            ('HN RSS', 'https://hnrss.org/frontpage'),
        ]
        
        for name, url in rss_feeds:
            self.fetchers.append(
                (name, RSSFetcher(url))
            )
    
    async def fetch_all(self) -> List[Article]:
        """
        Fetch from all sources concurrently.
        
        Returns:
            Combined list of all articles
        """
        print("\n🚀 Starting fetch from all sources...")
        print(f"   Sources: {len(self.fetchers)}")
        
        # Create tasks for all fetchers
        tasks = []
        for name, fetcher in self.fetchers:
            if isinstance(fetcher, HackerNewsFetcher):
                task = fetcher.fetch(limit=30)
            else:
                task = fetcher.fetch()
            tasks.append(task)
        
        # Fetch all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine articles
        all_articles = []
        for (name, _), result in zip(self.fetchers, results):
            if isinstance(result, Exception):
                print(f"⚠️  {name} failed: {result}")
            else:
                print(f"✅ {name}: {len(result)} articles")
                all_articles.extend(result)
        
        # Save combined results
        if all_articles:
            self.storage.save(all_articles, "all_articles.md")
        
        print(f"\n🎉 Total: {len(all_articles)} articles from {len(self.fetchers)} sources")
        return all_articles


# Test it
async def main():
    """Test orchestrator."""
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()
    
    print(f"\n📊 Sample articles:")
    for article in articles[:5]:
        print(f"  [{article.source}] {article.title[:60]}...")


if __name__ == "__main__":
    asyncio.run(main())
```

**Test orchestrator:**

```bash
python src/orchestrator.py

# Should fetch from all sources!
# Check data/articles/all_articles.md
```

---

### **Step 2: Create Main Entry Point (15 min)**

**Create:** `src/main.py`

```python
"""Main entry point for news fetcher."""
import asyncio
import sys
from src.orchestrator import FetchOrchestrator


async def main():
    """Main function."""
    print("=" * 60)
    print("  AI Agent Onboarding - News Fetcher")
    print("  Milestone 1: Async News Fetcher")
    print("=" * 60)
    
    try:
        # Run orchestrator
        orchestrator = FetchOrchestrator()
        articles = await orchestrator.fetch_all()
        
        print("\n" + "=" * 60)
        print(f"✅ Success! Fetched {len(articles)} articles total")
        print(f"📁 Saved to: data/articles/all_articles.md")
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

**Run the full system:**

```bash
python -m src.main

# Your complete news fetcher! 🎉
```

---

### **Step 3: Write Comprehensive Tests (45 min)**

**Update/create tests:**

```python
# tests/test_article.py
from src.models.article import Article
from datetime import datetime
import pytest


def test_article_creation():
    """Test creating article."""
    article = Article(
        title="Test",
        url="https://test.com",
        published_at=datetime.now(),
        source="test"
    )
    assert article.title == "Test"
    assert article.url == "https://test.com"


def test_article_validation():
    """Test article validation."""
    with pytest.raises(ValueError):
        Article(
            title="",  # Empty title should fail
            url="https://test.com",
            published_at=datetime.now(),
            source="test"
        )


def test_article_to_markdown():
    """Test markdown conversion."""
    article = Article(
        title="Test Article",
        url="https://test.com",
        published_at=datetime.now(),
        source="test",
        summary="Test summary"
    )
    
    md = article.to_markdown()
    assert "Test Article" in md
    assert "https://test.com" in md
    assert "test" in md
```

```python
# tests/test_storage.py
from src.storage.markdown_storage import MarkdownStorage
from src.models.article import Article
from datetime import datetime
import tempfile


def test_storage_save():
    """Test saving articles."""
    # Use temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = MarkdownStorage(tmpdir)
        
        article = Article(
            title="Test",
            url="https://test.com",
            published_at=datetime.now(),
            source="test"
        )
        
        path = storage.save([article], "test.md")
        
        assert path.exists()
        content = path.read_text()
        assert "Test" in content


def test_storage_multiple_articles():
    """Test saving multiple articles."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = MarkdownStorage(tmpdir)
        
        articles = [
            Article(f"Article {i}", f"https://test{i}.com", 
                   datetime.now(), "test")
            for i in range(5)
        ]
        
        path = storage.save(articles)
        content = path.read_text()
        
        assert "Article 0" in content
        assert "Article 4" in content
```

```python
# tests/test_orchestrator.py
import pytest
from src.orchestrator import FetchOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_fetch_all():
    """Test orchestrator fetches from all sources."""
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()
    
    # Should get some articles
    assert len(articles) > 0
    
    # Should have different sources
    sources = {a.source for a in articles}
    assert len(sources) > 1
```

---

### **Step 4: Check Test Coverage (15 min)**

**Run tests with coverage:**

```bash
# Install coverage if needed
pip install pytest-cov

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Should show coverage for each file
```

**Sample output:**

```
tests/test_article.py ........                                  [ 40%]
tests/test_hackernews_fetcher.py ..                             [ 50%]
tests/test_storage.py ...                                       [ 65%]
tests/test_orchestrator.py .                                    [ 70%]

----------- coverage: platform darwin, python 3.11.5 -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
src/models/article.py                      25      2    92%
src/fetchers/hackernews_fetcher.py         45      5    89%
src/fetchers/rss_fetcher.py                35      4    89%
src/storage/markdown_storage.py            20      1    95%
src/orchestrator.py                        30      3    90%
src/utils/rate_limiter.py                  15      2    87%
-----------------------------------------------------------
TOTAL                                     170     17    90%
```

**Target: 60%+ coverage** ✅

If under 60%, add more tests!

---

### **Evening 4 Deliverable:**

✅ Orchestrator coordinating all fetchers  
✅ Main entry point working  
✅ Comprehensive test suite  
✅ 60%+ test coverage  
✅ Complete working system!  

**Time used:** 1.5-2 hours

---

## 🌙 Evening 5: Polish & PR (Optional)

**⏰ Time:** 1 hour  
**Goal:** Final polish and create PR

### **Timeline:**

```
7:30 PM - Start
├── 7:30-7:50 PM (20 min) - Code cleanup
├── 7:50-8:10 PM (20 min) - Fix any issues
└── 8:10-8:30 PM (20 min) - Create PR
8:30 PM - Done!
```

---

### **Step 1: Code Cleanup (20 min)**

**Run linters:**

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check for issues
pylint src/
```

**Fix any warnings/errors.**

---

### **Step 2: Fix Issues (20 min)**

**Run final tests:**

```bash
pytest tests/ -v

# All should pass!
```

**Check files created:**

```bash
ls -lh data/articles/

# Should see markdown files
```

---

### **Step 3: Create PR (20 min)**

**Create PR description:**

```markdown
# Milestone 1: Async News Fetcher

## Summary

Built async news fetcher system that fetches from multiple sources concurrently.

## What I Built

✅ **2 Fetchers:**
- HackerNews API fetcher
- RSS feed fetcher

✅ **Infrastructure:**
- Article data model
- Markdown storage
- Rate limiting (10 concurrent max)
- Fetch orchestrator

✅ **Full async implementation:**
- Concurrent fetching (much faster!)
- Non-blocking I/O
- Graceful error handling

## Performance

- Fetches 30+ articles in ~2-3 seconds
- Concurrent fetching is ~5x faster than sequential
- Rate limiting prevents overwhelming servers

## Testing

- 60%+ test coverage
- Unit tests for all components
- Integration tests for full workflow
- Async tests passing

## Files Created

**Models:**
- src/models/article.py

**Fetchers:**
- src/fetchers/hackernews_fetcher.py
- src/fetchers/rss_fetcher.py

**Storage:**
- src/storage/markdown_storage.py

**Utils:**
- src/utils/rate_limiter.py

**Orchestration:**
- src/orchestrator.py
- src/main.py

**Tests:**
- tests/test_article.py
- tests/test_hackernews_fetcher.py
- tests/test_storage.py
- tests/test_orchestrator.py

## How to Run

```bash
# Run the fetcher
python -m src.main

# Run tests
pytest tests/ -v

# Check output
cat data/articles/all_articles.md
```

## Next Steps

Ready for Milestone 2: SOLID Refactoring

Will refactor this code to follow SOLID principles and add design patterns.

---

**Time spent:** 6-8 hours over 3-4 evenings  
**Lines of code:** ~400  
**Test coverage:** 60%+
```

**Submit PR:**

```bash
git add .
git commit -m "feat: async news fetcher with HackerNews and RSS support"
git push origin feature/milestone-1-async-fetcher
```

**Post in Slack:** `#ai-upskill-cohort-[X]`

```
📝 Milestone 1 PR ready for review!

Built async news fetcher that fetches from HackerNews and RSS concurrently.

✅ 2 fetchers working
✅ Full async implementation
✅ 60%+ test coverage
✅ Saves to markdown files

Link: [your PR URL]

Looking for 2 peer reviews! 🙏
```

---

### **Evening 5 Deliverable:**

✅ Code cleaned and formatted  
✅ All tests passing  
✅ PR created and submitted  
✅ Ready for Checkpoint 1 review!  

---

## 🎉 Milestone 1 Complete!

### **What You Accomplished:**

✅ Built first async Python code  
✅ Integrated with external APIs  
✅ Implemented concurrent fetching  
✅ Added rate limiting  
✅ Wrote comprehensive tests  
✅ Created production-ready component  

### **Skills Gained (12 skills):**

1. async/await fundamentals
2. aiohttp for HTTP requests
3. RSS feed parsing
4. Concurrent task execution
5. Rate limiting with Semaphore
6. Error handling in async code
7. Markdown file generation
8. Data modeling with dataclasses
9. Async testing with pytest
10. Test coverage measurement
11. Code organization
12. Integration testing

### **Performance Achievement:**

**Sequential fetching:** ~10-15 seconds  
**Your async fetching:** ~2-3 seconds  
**Speedup:** 5x faster! ⚡

---

## 📝 Checkpoint 1: PR Review

**Your PR will be reviewed for:**

✅ **Async Proficiency**
- Proper use of async/await
- Concurrent execution working
- No blocking operations

✅ **Code Quality**
- Clean, readable code
- Good error handling
- Proper abstractions

✅ **Testing**
- 60%+ coverage
- Tests passing
- Good test design

✅ **Functionality**
- Fetches from 2+ sources
- Saves to markdown
- Rate limiting works

**Required Approvals:** 2 reviewers

**See:** [Checkpoint 1 Rubric](../rubrics/checkpoint-1-rubric.md)

---

## ➡️ Next Steps

**After PR Approval:**

Proceed to [Milestone 2: SOLID Refactoring](milestone-2-solid-refactoring.md)

You'll refactor this code to follow professional software design principles!

**Time:** 4-5 evenings (8-10 hours)

---

**Questions?** Ask in Slack: `#ai-upskill-cohort-[X]`

**Milestone 1 Complete** ✅  
**Time Spent:** 6-8 hours over 3-4 evenings  
**Next:** Milestone 2 (Week 2)
