"""SQLite database manager for articles."""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import aiosqlite


class DatabaseManager:
    """Manages SQLite database for articles."""

    def __init__(self, db_path: str = "data/news_agent.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Create tables if they don't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    source TEXT NOT NULL,
                    published_at TEXT NOT NULL,
                    summary TEXT,
                    score INTEGER DEFAULT 0,
                    relevance_score INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_source ON articles(source)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_published ON articles(published_at)
            """)

            await db.commit()

        print(f"Database initialized: {self.db_path}", file=sys.stderr)

    async def insert_article(self, article: Dict):
        """Insert article into database."""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute(
                    """
                    INSERT INTO articles 
                    (title, url, source, published_at, summary, score, relevance_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        article["title"],
                        article["url"],
                        article["source"],
                        article["published_at"],
                        article.get("summary", ""),
                        article.get("score", 0),
                        article.get("relevance_score", 0),
                    ),
                )
                await db.commit()
            except sqlite3.IntegrityError:
                # URL already exists, skip
                pass

    async def query_articles(self, source: str = None, limit: int = 50) -> List[Dict]:
        """Query articles from database."""
        query = "SELECT * FROM articles"
        params = []

        if source:
            query += " WHERE source = ?"
            params.append(source)

        query += " ORDER BY published_at DESC LIMIT ?"
        params.append(limit)

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = sqlite3.Row
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]


# Test it
async def test_db():
    """Test database."""
    db = DatabaseManager()
    await db.initialize()

    # Insert test article
    await db.insert_article(
        {
            "title": "Test Article",
            "url": "https://test.com/article1",
            "source": "test",
            "published_at": datetime.now().isoformat(),
            "summary": "Test summary",
        }
    )

    # Query
    articles = await db.query_articles(limit=10)
    print(f"Found {len(articles)} articles")
    for article in articles:
        print(f"  - {article['title']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_db())
