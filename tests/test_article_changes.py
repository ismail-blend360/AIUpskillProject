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