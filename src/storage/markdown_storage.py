"""Save articles to markdown files."""
from typing import List
from pathlib import Path
from datetime import datetime
from src.models.article import Article
from src.storage.base_storage import ArticleStorage

class MarkdownStorage(ArticleStorage):
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