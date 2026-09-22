# Milestone 2: SOLID Refactoring

**⏰ Time Commitment:** 4-5 evenings (8-10 hours)  
**When:** Week 2, Days 6-10  
**Prerequisites:** Milestone 1 complete and PR merged  
**Checkpoint:** ✓ Checkpoint 2 (after completion)  
**Next Milestone:** [Milestone 3: First Agent with Tools](milestone-3-first-agent.md)

---

## 🎯 Learning Objectives

By the end of this week, you will:
- Apply all 5 SOLID principles to real code
- Refactor your Milestone 1 code to be professional-grade
- Implement 3 design patterns (Factory, Strategy, Template Method)
- **Prove extensibility:** Add GitHub Trending source WITHOUT modifying existing code
- Understand dependency injection
- Write more testable code

**This week transforms your "works" code into "professional" code!**

---

## 📚 Week 2 Overview

```
Week 2: Software Design Principles
├── Evening 6 (Mon): Single Responsibility Principle
│   └── Extract classes, one job per class
├── Evening 7 (Tue): Open/Closed Principle  
│   └── Create abstractions, add GitHub without changes
├── Evening 8 (Wed): Liskov + Interface Segregation
│   └── Substitutability + focused interfaces
├── Evening 9 (Thu): Dependency Inversion
│   └── Inject dependencies, loose coupling
├── Evening 10 (Fri): Design Patterns
│   └── Factory, Strategy, Template Method
└── Evening 11 (Mon): Documentation & PR
    └── Write design decisions, create PR

Total: 8-10 hours over 5-6 evenings
```

---

## 📖 Required Reading (Do First!)

**Before Evening 6, read these (1 hour total):**

1. **SOLID Principles Overview (20 min)**
   - https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
   - Quick, clear explanations

2. **Python SOLID Examples (20 min)**
   - https://realpython.com/solid-principles-python/
   - Python-specific examples

3. **Refactoring Catalog (20 min - skim)**
   - https://refactoring.guru/refactoring/techniques
   - Reference for when you refactor

**Done reading?** Start Evening 6! 🚀

---

## 🌙 Evening 6: Single Responsibility Principle

**⏰ Time:** 1.5-2 hours  
**Goal:** One class = one job

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:00 PM (30 min) - Analyze current code
├── 8:00-8:40 PM (40 min) - Extract ArticleTransformer
├── 8:40-9:10 PM (30 min) - Extract MarkdownStorage
└── 9:10-9:30 PM (20 min) - Update tests
9:30 PM - Done!
```

---

### **Step 1: Analyze Your Current Code (30 min)**

**Open your Milestone 1 code:**

```bash
# Look at your fetchers
code src/fetchers/hackernews_fetcher.py
code src/fetchers/rss_fetcher.py
```

**Identify responsibilities in HackerNewsFetcher:**

Current code probably looks like:

```python
class HackerNewsFetcher:
    """Fetches from HackerNews."""
    
    async def fetch(self) -> List[Article]:
        # 1. Fetch raw data from API
        raw_data = await self._fetch_from_hn_api()
        
        # 2. Transform data to Article objects
        articles = self._transform_hn_data(raw_data)
        
        # 3. Save to markdown files
        self._save_to_markdown(articles)
        
        return articles
    
    def _transform_hn_data(self, data):
        # Transform logic here
        ...
    
    def _save_to_markdown(self, articles):
        # File I/O logic here
        ...
```

**Problem:** This class has 3 responsibilities!
1. Fetching from HackerNews API
2. Transforming data
3. Saving to files

**SRP violation!** If file format changes, you edit the fetcher. Bad!

---

### **Step 2: Extract ArticleTransformer (40 min)**

**Create new file:** `src/transformers/article_transformer.py`

```python
"""Transform raw data to Article objects."""
from typing import List, Dict, Any
from datetime import datetime
from src.models.article import Article


class ArticleTransformer:
    """
    Transforms raw data from various sources to Article objects.
    
    Single Responsibility: Data transformation only.
    """
    
    def transform_hackernews(self, raw_data: List[Dict]) -> List[Article]:
        """
        Transform HackerNews API response to Articles.
        
        Args:
            raw_data: List of HN items from API
            
        Returns:
            List of Article objects
        """
        articles = []
        
        for item in raw_data:
            if not item.get('url'):
                continue
                
            article = Article(
                title=item.get('title', ''),
                url=item['url'],
                published_at=datetime.fromtimestamp(item.get('time', 0)),
                source='hackernews',
                summary=item.get('text', '')[:200] if item.get('text') else '',
                score=item.get('score', 0)
            )
            articles.append(article)
        
        return articles
    
    def transform_rss(self, entries: List[Any]) -> List[Article]:
        """
        Transform RSS feed entries to Articles.
        
        Args:
            entries: List of RSS entries from feedparser
            
        Returns:
            List of Article objects
        """
        articles = []
        
        for entry in entries:
            article = Article(
                title=entry.get('title', ''),
                url=entry.get('link', ''),
                published_at=self._parse_date(entry.get('published')),
                source='rss',
                summary=entry.get('summary', '')[:200]
            )
            articles.append(article)
        
        return articles
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse various date formats."""
        # Date parsing logic here
        # You can copy from your existing code
        try:
            from dateutil import parser
            return parser.parse(date_str)
        except:
            return datetime.now()
```

**Your task:**
1. Create this file (15 min)
2. Copy transformation logic from your fetchers (15 min)
3. Test it (10 min):

```python
# Quick test
from src.transformers.article_transformer import ArticleTransformer

transformer = ArticleTransformer()
raw_hn = [{'title': 'Test', 'url': 'http://example.com', 'time': 1234567890}]
articles = transformer.transform_hackernews(raw_hn)
assert len(articles) == 1
assert articles[0].title == 'Test'
print("✅ Transformer works!")
```

---

### **Step 3: Extract MarkdownStorage (30 min)**

**Create new file:** `src/storage/markdown_storage.py`

```python
"""Save articles to markdown files."""
from typing import List
from pathlib import Path
from datetime import datetime
from src.models.article import Article


class MarkdownStorage:
    """
    Saves articles to markdown files.
    
    Single Responsibility: File storage only.
    """
    
    def __init__(self, base_path: str = "data/articles"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, articles: List[Article], filename: str = None) -> Path:
        """
        Save articles to markdown file.
        
        Args:
            articles: List of articles to save
            filename: Optional filename, defaults to dated file
            
        Returns:
            Path to saved file
        """
        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"articles_{date_str}.md"
        
        filepath = self.base_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Articles - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            for article in articles:
                f.write(self._format_article(article))
                f.write("\n---\n\n")
        
        return filepath
    
    def _format_article(self, article: Article) -> str:
        """Format single article as markdown."""
        return f"""## {article.title}

**Source:** {article.source}
**URL:** {article.url}
**Published:** {article.published_at}
**Score:** {article.score if hasattr(article, 'score') else 'N/A'}

{article.summary}
"""
```

**Your task:**
1. Create this file (10 min)
2. Copy file I/O logic from your fetchers (10 min)
3. Test it (10 min):

```python
# Quick test
from src.storage.markdown_storage import MarkdownStorage
from src.models.article import Article
from datetime import datetime

storage = MarkdownStorage("data/test_articles")
test_article = Article(
    title="Test Article",
    url="http://test.com",
    published_at=datetime.now(),
    source="test",
    summary="Test summary"
)
path = storage.save([test_article], "test.md")
assert path.exists()
print(f"✅ Saved to {path}")
```

---

### **Step 4: Update Tests (20 min)**

**Update your fetcher tests:**

```python
# tests/test_hackernews_fetcher.py

import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


@pytest.mark.asyncio
async def test_hackernews_fetcher():
    """Test HackerNews fetcher with new architecture."""
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/test_articles")
    
    fetcher = HackerNewsFetcher(
        transformer=transformer,
        storage=storage
    )
    
    articles = await fetcher.fetch()
    
    assert len(articles) > 0
    assert all(hasattr(a, 'title') for a in articles)
```

**Run tests:**

```bash
pytest tests/test_hackernews_fetcher.py -v

# Should pass! ✅
```

---

### **Evening 6 Deliverable:**

✅ ArticleTransformer class (single responsibility: transform)  
✅ MarkdownStorage class (single responsibility: save)  
✅ Fetchers now only fetch (single responsibility)  
✅ Tests updated and passing  

**SRP Applied!** Each class has one job.

---

## 🌙 Evening 7: Open/Closed Principle

**⏰ Time:** 1.5-2 hours  
**Goal:** Open for extension, closed for modification

### **Timeline:**

```
7:30 PM - Start
├── 7:30-7:50 PM (20 min) - Create BaseFetcher ABC
├── 7:50-8:20 PM (30 min) - Refactor existing fetchers
├── 8:20-8:50 PM (30 min) - Add GitHub Trending (no changes!)
└── 8:50-9:10 PM (20 min) - Test and verify OCP
9:10 PM - Done!
```

---

### **Step 1: Create Abstract Base (20 min)**

**Create file:** `src/fetchers/base_fetcher.py`

```python
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
```

**Key points:**
- `@abstractmethod` = subclasses MUST implement
- Common logic in base class
- Specific logic in subclasses
- This is the **Template Method pattern**!

---

### **Step 2: Refactor Existing Fetchers (30 min)**

**Update HackerNewsFetcher:**

```python
# src/fetchers/hackernews_fetcher.py

from src.fetchers.base_fetcher import BaseFetcher
from typing import List
import aiohttp
from src.models.article import Article


class HackerNewsFetcher(BaseFetcher):
    """
    Fetch top stories from HackerNews.
    
    Inherits from BaseFetcher.
    Only implements source-specific logic.
    """
    
    async def fetch_articles(self) -> List[Article]:
        """Fetch from HackerNews API."""
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        
        async with aiohttp.ClientSession() as session:
            # Get top story IDs
            async with session.get(url) as response:
                story_ids = await response.json()
            
            # Fetch first 30 stories
            stories = []
            for story_id in story_ids[:30]:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                async with session.get(item_url) as response:
                    item = await response.json()
                    if item:
                        stories.append(item)
            
            # Transform using injected transformer
            return self.transformer.transform_hackernews(stories)
    
    def get_source_name(self) -> str:
        """Return source name."""
        return "hackernews"
```

**Do the same for RSSFetcher** (10 min):

```python
# src/fetchers/rss_fetcher.py

from src.fetchers.base_fetcher import BaseFetcher
import feedparser
from typing import List
from src.models.article import Article


class RSSFetcher(BaseFetcher):
    """Fetch from RSS feed."""
    
    def __init__(self, feed_url: str, transformer, storage):
        super().__init__(transformer, storage)
        self.feed_url = feed_url
    
    async def fetch_articles(self) -> List[Article]:
        """Fetch from RSS feed."""
        feed = feedparser.parse(self.feed_url)
        return self.transformer.transform_rss(feed.entries)
    
    def get_source_name(self) -> str:
        """Return source name."""
        return "rss"
```

---

### **Step 3: Add GitHub Trending WITHOUT Modifying Existing Code (30 min)**

**This is the OCP test!**

**Create NEW file:** `src/fetchers/github_trending_fetcher.py`

```python
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
```

**Install beautifulsoup4:**

```bash
pip install beautifulsoup4
```

**Test the new fetcher:**

```python
# Quick test
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage

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
```

---

### **Step 4: Verify OCP (20 min)**

**Check: Did you modify ANY existing files to add GitHub?**

Files you should NOT have touched:
- ❌ `hackernews_fetcher.py`
- ❌ `rss_fetcher.py`
- ❌ `base_fetcher.py` (except adding it initially)
- ❌ `article_transformer.py`
- ❌ `markdown_storage.py`

**If you didn't touch these files, you've proven OCP!** ✅

**Why this matters:**
- Added new functionality
- Zero risk of breaking existing code
- Can add unlimited new sources
- No regression testing needed for old code

**Update orchestrator to use new fetcher:**

```python
# src/orchestrator.py

from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher

class FetchOrchestrator:
    def __init__(self, transformer, storage):
        self.fetchers = [
            HackerNewsFetcher(transformer, storage),
            RSSFetcher("https://...", transformer, storage),
            GitHubTrendingFetcher(transformer, storage),  # Just add it!
        ]
```

**Run full fetch:**

```bash
python -m src.main

# Should fetch from all 3 sources!
# Check data/articles/ for markdown files
```

---

### **Evening 7 Deliverable:**

✅ BaseFetcher abstract class created  
✅ HackerNews and RSS inherit from BaseFetcher  
✅ **GitHub Trending added with ZERO changes to existing code** 🎯  
✅ All fetchers work identically  
✅ OCP proven!  

**Open/Closed Principle Applied!**

---

## 🌙 Evening 8: Liskov Substitution + Interface Segregation

**⏰ Time:** 2 hours  
**Goal:** Substitutability + focused interfaces

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:30 PM (60 min) - Liskov Substitution
└── 8:30-9:30 PM (60 min) - Interface Segregation
9:30 PM - Done!
```

---

### **Part 1: Liskov Substitution Principle (60 min)**

**Concept:** Any fetcher should work anywhere a BaseFetcher is expected.

### **Step 1: Write Substitutability Test (20 min)**

**Create test:** `tests/test_substitutability.py`

```python
"""Test Liskov Substitution Principle."""
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


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
        GitHubTrendingFetcher(transformer, storage)
    ]
    
    # Each fetcher should work identically
    for fetcher in fetchers:
        # Should have same interface
        assert hasattr(fetcher, 'fetch_articles')
        assert hasattr(fetcher, 'get_source_name')
        assert hasattr(fetcher, 'fetch_and_save')
        
        # Should return List[Article]
        articles = await fetcher.fetch_articles()
        assert isinstance(articles, list)
        
        # All articles should have same structure
        if articles:
            article = articles[0]
            assert hasattr(article, 'title')
            assert hasattr(article, 'url')
            assert hasattr(article, 'source')
        
        # Should have source name
        source = fetcher.get_source_name()
        assert isinstance(source, str)
        assert len(source) > 0
    
    print("✅ All fetchers are substitutable!")
```

**Run the test:**

```bash
pytest tests/test_substitutability.py -v

# Should pass for all fetchers!
```

---

### **Step 2: Fix Any LSP Violations (20 min)**

**Common violations to check:**

**Violation 1: Different return types**
```python
# BAD - violates LSP
class BadFetcher(BaseFetcher):
    async def fetch_articles(self):
        return None  # Wrong! Should return List[Article]
```

**Fix:** Always return List[Article], even if empty
```python
# GOOD
async def fetch_articles(self) -> List[Article]:
    return []  # Empty list, not None
```

**Violation 2: Throwing unexpected errors**
```python
# BAD
async def fetch_articles(self):
    raise NotImplementedError()  # Violates contract!
```

**Fix:** Handle errors internally
```python
# GOOD
async def fetch_articles(self) -> List[Article]:
    try:
        # fetch logic
        ...
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        return []  # Return empty list on error
```

**Check your fetchers** - fix any violations.

---

### **Step 3: Test Polymorphism (20 min)**

**Add this test:**

```python
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
```

---

### **Part 2: Interface Segregation Principle (60 min)**

**Concept:** Don't force classes to implement methods they don't need.

### **Step 1: Identify Fat Interfaces (15 min)**

**Question:** Do all fetchers need the same methods?

Currently:
- `fetch_articles()` - Yes, all need this
- `get_source_name()` - Yes, all need this
- `fetch_and_save()` - Yes, all need this

**What about:**
- `authenticate()` - Only some sources need auth
- `paginate()` - Only some sources paginate
- `rate_limit()` - Only some sources rate limit

**Don't add these to BaseFetcher!** Only add what ALL fetchers need.

---

### **Step 2: Create Optional Interfaces (25 min)**

**For auth-required sources:**

```python
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
```

**Usage:**

```python
# Future fetcher that needs auth
class TwitterFetcher(BaseFetcher, AuthenticatedFetcher):
    """
    Fetch from Twitter API.
    
    Implements both BaseFetcher and AuthenticatedFetcher.
    """
    
    async def fetch_articles(self):
        # First authenticate
        if not await self.authenticate():
            return []
        
        # Then fetch
        ...
    
    async def authenticate(self):
        # Twitter-specific auth
        ...
```

**Key point:** Twitter gets auth, but HackerNews doesn't have to implement unused methods!

---

### **Step 3: Verify ISP (20 min)**

**Check your BaseFetcher:**

```python
# Count methods in BaseFetcher
# Should be minimal - only what ALL fetchers need

class BaseFetcher(ABC):
    # These 3 methods - ALL fetchers need them ✅
    async def fetch_articles(self) -> List[Article]: ...
    def get_source_name(self) -> str: ...
    async def fetch_and_save(self) -> List[Article]: ...
    
    # DON'T add these unless ALL fetchers need them:
    # ❌ async def authenticate(self): ...
    # ❌ async def fetch_page(self, page: int): ...
    # ❌ async def rate_limit(self): ...
```

**If your BaseFetcher only has 3-4 methods, you're following ISP!** ✅

---

### **Evening 8 Deliverable:**

✅ Substitutability test passing  
✅ All fetchers can be used interchangeably  
✅ LSP violations fixed  
✅ Optional interfaces created (AuthenticatedFetcher, etc)  
✅ BaseFetcher has minimal interface  
✅ ISP applied!  

**LSP + ISP Applied!**

---

## 🌙 Evening 9: Dependency Inversion Principle

**⏰ Time:** 1.5-2 hours  
**Goal:** Depend on abstractions, inject dependencies

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:00 PM (30 min) - Create storage interface
├── 8:00-8:30 PM (30 min) - Refactor orchestrator with DI
├── 8:30-9:00 PM (30 min) - Test with dependency injection
└── 9:00-9:30 PM (30 min) - Write tests with mocks
9:30 PM - Done!
```

---

### **Step 1: Create Storage Interface (30 min)**

**Current problem:** Code depends on concrete `MarkdownStorage` class.

**Solution:** Depend on abstraction.

**Create:** `src/storage/base_storage.py`

```python
"""Storage interface."""
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
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
```

**Update MarkdownStorage:**

```python
# src/storage/markdown_storage.py

from src.storage.base_storage import ArticleStorage

class MarkdownStorage(ArticleStorage):  # Inherit from interface
    """Markdown implementation of ArticleStorage."""
    
    def save(self, articles: List[Article], filename: str = None) -> Path:
        # Same implementation as before
        ...
```

**Now you could create other implementations:**

```python
class JSONStorage(ArticleStorage):
    """Save articles as JSON."""
    def save(self, articles, filename=None):
        # JSON implementation
        ...

class DatabaseStorage(ArticleStorage):
    """Save articles to database."""
    def save(self, articles, filename=None):
        # Database implementation
        ...
```

**Fetchers don't care!** They just use `ArticleStorage` interface.

---

### **Step 2: Refactor Orchestrator with Dependency Injection (30 min)**

**Before (tight coupling):**

```python
class FetchOrchestrator:
    def __init__(self):
        # Depends on concrete classes! ❌
        self.transformer = ArticleTransformer()
        self.storage = MarkdownStorage()
        self.fetchers = [
            HackerNewsFetcher(self.transformer, self.storage),
            ...
        ]
```

**After (dependency injection):**

```python
# src/orchestrator.py

from typing import List
from src.fetchers.base_fetcher import BaseFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.base_storage import ArticleStorage


class FetchOrchestrator:
    """
    Orchestrates multiple fetchers.
    
    Follows Dependency Inversion Principle:
    - Depends on abstractions (BaseFetcher, ArticleStorage)
    - Dependencies injected via constructor
    """
    
    def __init__(
        self,
        fetchers: List[BaseFetcher],
        storage: ArticleStorage,
        transformer: ArticleTransformer
    ):
        """
        Initialize with injected dependencies.
        
        Args:
            fetchers: List of fetcher instances
            storage: Storage implementation
            transformer: Transformer instance
        """
        self.fetchers = fetchers
        self.storage = storage
        self.transformer = transformer
    
    async def fetch_all(self) -> List[Article]:
        """Fetch from all sources."""
        all_articles = []
        
        for fetcher in self.fetchers:
            articles = await fetcher.fetch_and_save()
            all_articles.extend(articles)
        
        return all_articles
```

**Usage in main.py:**

```python
# src/main.py

from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


async def main():
    """Main entry point with dependency injection."""
    
    # Create dependencies
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")
    
    # Create fetchers
    fetchers = [
        HackerNewsFetcher(transformer, storage),
        GitHubTrendingFetcher(transformer, storage),
    ]
    
    # Inject dependencies into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=fetchers,
        storage=storage,
        transformer=transformer
    )
    
    # Run
    articles = await orchestrator.fetch_all()
    print(f"✅ Fetched {len(articles)} articles total")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Benefits:**
- Easy to swap implementations
- Easy to test with mocks
- Loose coupling
- Flexible

---

### **Step 3: Test Dependency Injection (30 min)**

**Run your main:**

```bash
python -m src.main

# Should work exactly as before!
# But now with better architecture
```

**Test flexibility - swap storage:**

```python
# Can easily switch storage implementation
from src.storage.json_storage import JSONStorage  # If you made it

# Just change one line:
storage = JSONStorage("data/articles_json")

# Everything else stays the same!
```

---

### **Step 4: Write Tests with Mocks (30 min)**

**This is where DIP really shines!**

```python
# tests/test_orchestrator.py

import pytest
from unittest.mock import Mock, AsyncMock
from src.orchestrator import FetchOrchestrator
from src.models.article import Article
from datetime import datetime


@pytest.mark.asyncio
async def test_orchestrator_with_mocks():
    """
    Test orchestrator with mocked dependencies.
    
    DIP makes this easy - just inject mocks!
    """
    # Create mock fetcher
    mock_fetcher = Mock()
    mock_fetcher.fetch_and_save = AsyncMock(return_value=[
        Article(
            title="Test",
            url="http://test.com",
            published_at=datetime.now(),
            source="test",
            summary="Test"
        )
    ])
    
    # Create mock storage
    mock_storage = Mock()
    
    # Create mock transformer
    mock_transformer = Mock()
    
    # Inject mocks into orchestrator
    orchestrator = FetchOrchestrator(
        fetchers=[mock_fetcher],
        storage=mock_storage,
        transformer=mock_transformer
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
    mock_fetcher1.fetch_and_save = AsyncMock(return_value=[
        Article(title="Article 1", url="http://1.com", 
                published_at=datetime.now(), source="test", summary="Test")
    ])
    
    mock_fetcher2 = Mock()
    mock_fetcher2.fetch_and_save = AsyncMock(return_value=[
        Article(title="Article 2", url="http://2.com",
                published_at=datetime.now(), source="test", summary="Test")
    ])
    
    orchestrator = FetchOrchestrator(
        fetchers=[mock_fetcher1, mock_fetcher2],
        storage=Mock(),
        transformer=Mock()
    )
    
    articles = await orchestrator.fetch_all()
    
    assert len(articles) == 2
    print("✅ Multiple fetchers work!")
```

**Run tests:**

```bash
pytest tests/test_orchestrator.py -v

# Should pass!
# Notice: No real HTTP calls needed
# No real file I/O needed
# Fast, isolated tests!
```

---

### **Evening 9 Deliverable:**

✅ ArticleStorage interface created  
✅ Dependencies injected via constructors  
✅ Orchestrator depends on abstractions  
✅ Easy to swap implementations  
✅ Tests use mocks (fast, isolated)  
✅ DIP applied!  

**Dependency Inversion Principle Applied!**

---

## 🌙 Evening 10: Design Patterns

**⏰ Time:** 1.5-2 hours  
**Goal:** Apply Factory, Strategy, and Template Method patterns

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:00 PM (30 min) - Factory Pattern
├── 8:00-8:30 PM (30 min) - Strategy Pattern
├── 8:30-9:00 PM (30 min) - Template Method (review)
└── 9:00-9:30 PM (30 min) - Test all patterns
9:30 PM - Done!
```

---

### **Pattern 1: Factory Pattern (30 min)**

**Problem:** Creating fetchers manually is repetitive.

**Solution:** Factory creates them for you.

**Create:** `src/factories/fetcher_factory.py`

```python
"""Factory for creating fetchers."""
from typing import Dict, Type
from src.fetchers.base_fetcher import BaseFetcher
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher


class FetcherFactory:
    """
    Factory for creating fetcher instances.
    
    Implements Factory pattern.
    """
    
    # Registry of available fetchers
    _fetchers: Dict[str, Type[BaseFetcher]] = {
        'hackernews': HackerNewsFetcher,
        'github': GitHubTrendingFetcher,
    }
    
    @classmethod
    def create(
        cls,
        source_type: str,
        transformer,
        storage,
        **kwargs
    ) -> BaseFetcher:
        """
        Create fetcher by type.
        
        Args:
            source_type: Type of fetcher ('hackernews', 'github', etc.)
            transformer: Transformer instance
            storage: Storage instance
            **kwargs: Additional args for specific fetchers
            
        Returns:
            Fetcher instance
            
        Raises:
            ValueError: If source_type unknown
        """
        if source_type not in cls._fetchers:
            raise ValueError(f"Unknown fetcher type: {source_type}")
        
        fetcher_class = cls._fetchers[source_type]
        
        # Special case for RSS which needs URL
        if source_type == 'rss':
            feed_url = kwargs.get('feed_url')
            if not feed_url:
                raise ValueError("RSS fetcher requires feed_url")
            return RSSFetcher(feed_url, transformer, storage)
        
        # Standard creation
        return fetcher_class(transformer, storage)
    
    @classmethod
    def register(cls, name: str, fetcher_class: Type[BaseFetcher]):
        """
        Register new fetcher type.
        
        Allows extending factory without modifying it (OCP!).
        """
        cls._fetchers[name] = fetcher_class
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of available fetcher types."""
        return list(cls._fetchers.keys())
```

**Usage:**

```python
# Before (manual creation):
hn_fetcher = HackerNewsFetcher(transformer, storage)
gh_fetcher = GitHubTrendingFetcher(transformer, storage)

# After (factory):
hn_fetcher = FetcherFactory.create('hackernews', transformer, storage)
gh_fetcher = FetcherFactory.create('github', transformer, storage)

# Even better - create from config:
config_sources = ['hackernews', 'github']
fetchers = [
    FetcherFactory.create(source, transformer, storage)
    for source in config_sources
]
```

---

### **Pattern 2: Strategy Pattern for Rate Limiting (30 min)**

**Problem:** Different sources need different rate limiting strategies.

**Solution:** Strategy pattern - swap rate limiting strategies.

**Create:** `src/strategies/rate_limit_strategy.py`

```python
"""Rate limiting strategies."""
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime, timedelta


class RateLimitStrategy(ABC):
    """Abstract strategy for rate limiting."""
    
    @abstractmethod
    async def acquire(self):
        """Acquire permission to make request."""
        pass
    
    @abstractmethod
    def release(self):
        """Release permission after request."""
        pass


class SemaphoreStrategy(RateLimitStrategy):
    """
    Simple semaphore-based rate limiting.
    
    Limits concurrent requests.
    """
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def acquire(self):
        await self.semaphore.acquire()
    
    def release(self):
        self.semaphore.release()


class TokenBucketStrategy(RateLimitStrategy):
    """
    Token bucket rate limiting.
    
    Allows bursts but limits over time.
    """
    
    def __init__(self, rate: int, per: float):
        """
        Initialize token bucket.
        
        Args:
            rate: Number of requests
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = datetime.now()
    
    async def acquire(self):
        current = datetime.now()
        time_passed = (current - self.last_check).total_seconds()
        self.last_check = current
        
        self.allowance += time_passed * (self.rate / self.per)
        if self.allowance > self.rate:
            self.allowance = self.rate
        
        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0
    
    def release(self):
        pass  # Not needed for token bucket
```

**Usage in fetcher:**

```python
class HackerNewsFetcher(BaseFetcher):
    def __init__(self, transformer, storage, rate_limiter=None):
        super().__init__(transformer, storage)
        # Use provided strategy or default
        self.rate_limiter = rate_limiter or SemaphoreStrategy(10)
    
    async def fetch_articles(self):
        await self.rate_limiter.acquire()
        try:
            # Fetch logic
            ...
        finally:
            self.rate_limiter.release()
```

**Flexibility:**

```python
# Use different strategies for different sources
hn_fetcher = HackerNewsFetcher(
    transformer, storage,
    rate_limiter=SemaphoreStrategy(5)  # 5 concurrent
)

gh_fetcher = GitHubTrendingFetcher(
    transformer, storage,
    rate_limiter=TokenBucketStrategy(100, 60)  # 100 per minute
)
```

---

### **Pattern 3: Template Method (Review) (30 min)**

**You already implemented this!** Let's review.

**In BaseFetcher:**

```python
class BaseFetcher(ABC):
    # Template method
    async def fetch_and_save(self) -> List[Article]:
        """
        Template method - defines algorithm skeleton.
        
        Steps:
        1. Fetch (varies by subclass)
        2. Save (same for all)
        
        Subclasses customize step 1 via fetch_articles().
        """
        # Step 1: Fetch (customizable)
        articles = await self.fetch_articles()
        
        # Step 2: Save (same for all)
        if articles:
            filename = f"{self.get_source_name()}_articles.md"
            self.storage.save(articles, filename)
        
        return articles
    
    @abstractmethod
    async def fetch_articles(self):
        """Customization point - varies by source."""
        pass
```

**This is Template Method pattern:**
- Base class defines algorithm structure
- Subclasses fill in specific steps
- Ensures consistent behavior

---

### **Step 4: Test All Patterns (30 min)**

**Test factory:**

```python
def test_factory():
    """Test factory pattern."""
    transformer = ArticleTransformer()
    storage = MarkdownStorage()
    
    # Create via factory
    fetcher = FetcherFactory.create('hackernews', transformer, storage)
    
    assert isinstance(fetcher, HackerNewsFetcher)
    assert fetcher.get_source_name() == 'hackernews'
    
    # List available types
    types = FetcherFactory.get_available_types()
    assert 'hackernews' in types
    assert 'github' in types
    
    print("✅ Factory works!")
```

**Test strategy:**

```python
async def test_rate_limiting():
    """Test rate limiting strategies."""
    import time
    
    # Semaphore - allows 2 concurrent
    sem_strategy = SemaphoreStrategy(2)
    
    async def task():
        await sem_strategy.acquire()
        await asyncio.sleep(0.1)
        sem_strategy.release()
    
    start = time.time()
    await asyncio.gather(*[task() for _ in range(4)])
    elapsed = time.time() - start
    
    # Should take ~0.2s (2 at a time, 0.1s each)
    assert elapsed >= 0.2
    assert elapsed < 0.3
    
    print("✅ Rate limiting works!")
```

**Run:**

```bash
pytest tests/test_patterns.py -v
```

---

### **Evening 10 Deliverable:**

✅ Factory pattern implemented  
✅ Strategy pattern for rate limiting  
✅ Template Method reviewed  
✅ All patterns tested  
✅ Code is extensible and maintainable  

**Design Patterns Applied!**

---

## 🌙 Evening 11: Documentation & PR

**⏰ Time:** 1 hour  
**Goal:** Document your work and create PR

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:00 PM (30 min) - Write design decisions
└── 8:00-8:30 PM (30 min) - Create PR
8:30 PM - Done!
```

---

### **Step 1: Write Design Decisions (30 min)**

**Create:** `docs/design-decisions.md`

```markdown
# Design Decisions - Milestone 2 Refactoring

## Summary

Refactored Milestone 1 codebase to follow SOLID principles and design patterns.

## Changes Made

### 1. Single Responsibility Principle

**Problem:** Fetchers had multiple responsibilities (fetch, transform, save)

**Solution:**
- Extracted `ArticleTransformer` class (responsibility: transform data)
- Extracted `MarkdownStorage` class (responsibility: save to files)
- Fetchers now only fetch (single responsibility)

**Benefit:** Changes to transformation logic don't affect fetchers

### 2. Open/Closed Principle

**Problem:** Adding new source required modifying existing code

**Solution:**
- Created `BaseFetcher` abstract base class
- All fetchers inherit from BaseFetcher
- New sources extend without modifying existing

**Proof:** Added GitHub Trending with ZERO changes to existing code

**Benefit:** New sources can be added safely, no regression risk

### 3. Liskov Substitution Principle

**Problem:** Fetchers had inconsistent interfaces

**Solution:**
- Defined clear contract in BaseFetcher
- All fetchers implement same interface
- Substitutability tests ensure compliance

**Benefit:** Any fetcher can be used anywhere BaseFetcher is expected

### 4. Interface Segregation Principle

**Problem:** Risk of fat interfaces forcing unused methods

**Solution:**
- BaseFetcher has minimal interface (3 methods)
- Optional interfaces for special cases (AuthenticatedFetcher, etc.)
- Fetchers only implement what they need

**Benefit:** Clean, focused interfaces

### 5. Dependency Inversion Principle

**Problem:** Classes depended on concrete implementations

**Solution:**
- Created `ArticleStorage` interface
- Dependencies injected via constructors
- Code depends on abstractions

**Benefit:** Easy to test (inject mocks), easy to swap implementations

## Design Patterns Applied

### Factory Pattern

**Location:** `src/factories/fetcher_factory.py`

**Purpose:** Create fetchers without knowing concrete classes

**Usage:**
```python
fetcher = FetcherFactory.create('hackernews', transformer, storage)
```

**Benefit:** Configuration-driven fetcher creation

### Strategy Pattern

**Location:** `src/strategies/rate_limit_strategy.py`

**Purpose:** Swap rate limiting algorithms

**Usage:**
```python
fetcher = HackerNewsFetcher(
    transformer, storage,
    rate_limiter=TokenBucketStrategy(100, 60)
)
```

**Benefit:** Different strategies for different sources

### Template Method Pattern

**Location:** `src/fetchers/base_fetcher.py` (fetch_and_save method)

**Purpose:** Define algorithm skeleton, allow customization

**Benefit:** Consistent behavior across all fetchers

## Metrics

### Before Refactoring
- Classes: 2 (HackerNewsFetcher, RSSFetcher)
- Responsibilities per class: ~3
- Extensibility: Requires modifying existing code
- Testability: Hard (concrete dependencies)

### After Refactoring
- Classes: 8 (fetchers, transformer, storage, factory)
- Responsibilities per class: 1
- Extensibility: Add new sources with zero existing code changes
- Testability: Easy (dependency injection, mocks)

## Trade-offs

### More Classes
- **Con:** More files to navigate
- **Pro:** Each class is simple and focused

### More Abstraction
- **Con:** Slightly more complex for beginners
- **Pro:** Much easier to maintain and extend

### Dependency Injection
- **Con:** More setup code
- **Pro:** Much easier to test

## Lessons Learned

1. **SRP makes code easier to change** - When file format needs to change, only touch MarkdownStorage
2. **OCP proven by GitHub addition** - Added complete new source with zero risk
3. **DIP makes testing easy** - Can test orchestrator without real HTTP calls
4. **Design patterns solve real problems** - Not just theory, actually useful

## Next Steps

These patterns will be used in upcoming milestones:
- Milestone 3: Agents will use DIP
- Milestone 4: MCP servers will use Factory pattern
- Milestone 5: Evaluation will benefit from SRP

---

*Last updated: [Your date]*
*By: [Your name]*
```

---

### **Step 2: Create PR (30 min)**

**Create PR description:**

```markdown
# Milestone 2: SOLID Refactoring

## Summary

Refactored Milestone 1 codebase to follow SOLID principles and design patterns.

## Changes

### SOLID Principles Applied

✅ **Single Responsibility Principle**
- Extracted ArticleTransformer (one responsibility: transform)
- Extracted MarkdownStorage (one responsibility: save)
- Fetchers now only fetch

✅ **Open/Closed Principle**
- Created BaseFetcher abstract class
- Added GitHub Trending with **zero changes** to existing code 🎯

✅ **Liskov Substitution Principle**
- All fetchers implement same contract
- Substitutability tests passing

✅ **Interface Segregation Principle**
- BaseFetcher has minimal interface
- Optional interfaces for special cases

✅ **Dependency Inversion Principle**
- Dependencies injected via constructors
- Code depends on abstractions (ArticleStorage, BaseFetcher)

### Design Patterns Implemented

✅ **Factory Pattern** - FetcherFactory for creating fetchers  
✅ **Strategy Pattern** - RateLimitStrategy for different algorithms  
✅ **Template Method** - BaseFetcher.fetch_and_save()  

## Proof of Open/Closed Principle

GitHub Trending source added in commit [hash] with **zero modifications** to:
- ❌ hackernews_fetcher.py (not touched)
- ❌ rss_fetcher.py (not touched)
- ❌ article_transformer.py (not touched)
- ❌ markdown_storage.py (not touched)

Only added new file: `github_trending_fetcher.py` ✅

## Testing

- All existing tests still pass ✅
- New substitutability tests added ✅
- Mock-based tests using DI ✅
- Coverage maintained at 60%+ ✅

## Files Changed

**Added:**
- src/fetchers/base_fetcher.py (Abstract base class)
- src/fetchers/github_trending_fetcher.py (New source)
- src/transformers/article_transformer.py (Extracted)
- src/storage/base_storage.py (Interface)
- src/storage/markdown_storage.py (Refactored)
- src/factories/fetcher_factory.py (Factory)
- src/strategies/rate_limit_strategy.py (Strategy)
- tests/test_substitutability.py (LSP tests)
- docs/design-decisions.md (Documentation)

**Modified:**
- src/fetchers/hackernews_fetcher.py (Now extends BaseFetcher)
- src/fetchers/rss_fetcher.py (Now extends BaseFetcher)
- src/orchestrator.py (Uses DI)
- src/main.py (Sets up DI)

## How to Review

1. **Check SOLID compliance:**
   - Each class has single responsibility
   - GitHub added without modifying existing
   - Tests use mocks (DIP working)

2. **Run tests:**
   ```bash
   pytest tests/ -v
   # All should pass
   ```

3. **Try adding new source:**
   - Should be able to create new fetcher
   - Without touching existing code
   - Just extend BaseFetcher

4. **Check design decisions doc:**
   - Read docs/design-decisions.md
   - Verify reasoning is sound

## Checklist

- [x] All 5 SOLID principles applied
- [x] 3 design patterns implemented
- [x] GitHub Trending added without modifying existing code
- [x] All tests passing
- [x] Design decisions documented
- [x] Code follows style guide
- [x] Ready for Checkpoint 2 review

## Questions for Reviewers

1. Is the abstraction level appropriate?
2. Are there any remaining SOLID violations?
3. Is dependency injection clear?
4. Should we add more design patterns?

---

**Time spent:** ~8-10 hours over 5-6 evenings  
**Ready for:** Checkpoint 2 review  
**Next milestone:** First Agent with Tools
```

**Submit PR:**

```bash
git add .
git commit -m "feat: refactor with SOLID principles and design patterns"
git push origin feature/milestone-2-solid
```

Create PR on GitHub and post in Slack!

---

### **Evening 11 Deliverable:**

✅ Design decisions documented  
✅ PR description complete  
✅ PR submitted for review  
✅ Checkpoint 2 ready!  

---

## 🎉 Milestone 2 Complete!

### **What You Accomplished This Week:**

✅ Applied all 5 SOLID principles to real code  
✅ Implemented 3 design patterns  
✅ Refactored working code to be professional-grade  
✅ **Proved extensibility** by adding GitHub with zero changes  
✅ Made code highly testable with dependency injection  
✅ Documented design decisions  

### **Skills Gained:**

**Software Design (18 skills):**
1-5. All 5 SOLID principles  
6-8. Factory, Strategy, Template Method patterns  
9-11. Code smell identification, refactoring techniques  
12-14. Dependency injection, interface design  
15-16. Substitutability testing, mock-based testing  
17-18. Design documentation, technical writing  

### **Code Quality:**

**Before:** Works, but coupled and hard to extend  
**After:** Professional-grade, extensible, testable  

**Proof:** GitHub Trending added with **zero changes** to existing code! 🎯

---

## 📝 Checkpoint 2: PR Review

**Your PR will be reviewed for:**

✅ **SOLID Compliance**
- Each class single responsibility
- Open/Closed proven (GitHub added cleanly)
- Substitutability tests pass
- Interfaces focused
- Dependencies injected

✅ **Design Patterns**
- Factory correctly implemented
- Strategy pattern working
- Template Method clear

✅ **Code Quality**
- Clean, readable code
- Proper abstractions
- Good naming
- Tests passing

✅ **Documentation**
- Design decisions explained
- Patterns justified
- Trade-offs discussed

**Required Approvals:** 2 reviewers

**See:** [Checkpoint 2 Rubric](../rubrics/checkpoint-2-rubric.md)

---

## ➡️ Next Steps

**After PR Approval:**

Proceed to [Milestone 3: First Agent with Tools](milestone-3-first-agent.md)

You'll build your first AI agent using the clean architecture you just created!

**Time:** 4-5 evenings (8-10 hours)

**What you'll learn:**
- AI agent architecture
- LiteLLM integration (provider-agnostic LLM access)
- Prompt engineering
- Function calling / tool use

**Get some rest!** You earned it. Week 3 starts tomorrow! 🚀

---

**Questions?** Ask in Slack: `#ai-agent-onboarding-cohort-[X]`

**Milestone 2 Complete** ✅  
**Time Spent:** 8-10 hours over 5-6 evenings  
**Next:** Milestone 3 (Week 3)
