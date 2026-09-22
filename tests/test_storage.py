# tests/test_storage.py
import tempfile
from datetime import datetime

from src.models.article import Article
from src.storage.markdown_storage import MarkdownStorage


def test_storage_save():
    """Test saving articles."""
    # Use temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = MarkdownStorage(tmpdir)

        article = Article(
            title="Test",
            url="https://test.com",
            published_at=datetime.now(),
            source="test",
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
            Article(f"Article {i}", f"https://test{i}.com", datetime.now(), "test")
            for i in range(5)
        ]

        path = storage.save(articles)
        content = path.read_text()

        assert "Article 0" in content
        assert "Article 4" in content
