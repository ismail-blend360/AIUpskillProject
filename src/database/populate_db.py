# populate_db.py
import asyncio
import re
from datetime import datetime
from pathlib import Path

from src.database.db_manager import DatabaseManager


async def populate_from_markdown():
    """Populate database from markdown files."""
    db = DatabaseManager()
    await db.initialize()

    # Read articles from markdown
    articles_dir = Path("data/articles")

    for md_file in articles_dir.glob("*.md"):
        print(f"Reading {md_file.name}...")
        content = md_file.read_text(encoding="utf-8")

        # Simple parsing
        sections = content.split("---")

        for section in sections:
            if "##" not in section:
                continue

            # Extract title
            title_match = re.search(r"## (.+)", section)
            if not title_match:
                continue
            title = title_match.group(1).strip()

            # Extract URL
            url_match = re.search(r"\*\*URL:\*\* (.+)", section)
            if not url_match:
                continue
            url = url_match.group(1).strip()

            # Extract source
            source_match = re.search(r"\*\*Source:\*\* (.+)", section)
            source = source_match.group(1).strip() if source_match else "unknown"

            # Extract summary
            lines = [
                l for l in section.split("\n") if l.strip() and not l.startswith("**")
            ]
            summary = lines[-1] if lines else ""

            # Insert
            await db.insert_article(
                {
                    "title": title,
                    "url": url,
                    "source": source,
                    "published_at": datetime.now().isoformat(),
                    "summary": summary,
                }
            )

    # Check count
    articles = await db.query_articles(limit=1000)
    print(f"\n✅ Database populated with {len(articles)} articles")


if __name__ == "__main__":
    asyncio.run(populate_from_markdown())
