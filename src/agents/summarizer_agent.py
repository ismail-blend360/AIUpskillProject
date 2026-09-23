"""Agent that summarizes filtered articles."""

import re
from pathlib import Path
from typing import Any, Dict

from src.agents.base_agent import BaseAgent
from src.skills.search_skill import SearchSkill


class SummarizerAgent(BaseAgent):
    """
    Summarizes filtered articles into daily digest.

    Can use SearchSkill to find additional context.
    """

    def __init__(self):
        super().__init__()
        self.search_skill = SearchSkill()

    async def _load_context(self, input_path: str) -> Dict[str, Any]:
        """Load filtered articles."""
        print(f"📖 Loading filtered articles from {input_path}")

        content = Path(input_path).read_text(encoding="utf-8")

        # Parse articles
        articles = self._parse_markdown(content)

        print(f"   Found {len(articles)} filtered articles")
        return {"articles": articles}

    def _parse_markdown(self, content: str) -> list[Dict]:
        """Parse markdown to extract articles."""
        articles = []
        sections = content.split("---")

        for section in sections:
            if "##" not in section:
                continue

            title_match = re.search(r"## (.+)", section)
            if not title_match:
                continue

            title = title_match.group(1).strip()

            # Extract relevance score
            score_match = re.search(r"\*\*Relevance Score:\*\* (\d+)", section)
            relevance = int(score_match.group(1)) if score_match else 0

            # Extract reasoning
            reason_match = re.search(r"\*\*Reasoning:\*\* (.+)", section)
            reasoning = reason_match.group(1).strip() if reason_match else ""

            # Extract topics
            topics_match = re.search(r"\*\*Key Topics:\*\* (.+)", section)
            topics = topics_match.group(1).strip() if topics_match else ""

            articles.append(
                {
                    "title": title,
                    "relevance": relevance,
                    "reasoning": reasoning,
                    "topics": topics,
                }
            )

        return articles

    async def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize articles."""
        articles = context["articles"]

        print(f"📝 Summarizing {len(articles)} articles...")

        # Group by topic
        topics = {}
        for article in articles:
            topic = article["topics"].split(",")[0] if article["topics"] else "Other"
            topic = topic.strip()

            if topic not in topics:
                topics[topic] = []
            topics[topic].append(article)

        # Generate summary for each topic
        summaries = {}
        for topic, topic_articles in topics.items():
            print(f"   Summarizing {topic}: {len(topic_articles)} articles")
            summary = await self._summarize_topic(topic, topic_articles)
            summaries[topic] = summary

        return {
            "topics": topics,
            "summaries": summaries,
            "total_articles": len(articles),
        }

    async def _summarize_topic(self, topic: str, articles: list[Dict]) -> str:
        """Generate summary for a topic."""
        # Create prompt
        articles_text = "\n".join(
            [f"- {a['title']}: {a['reasoning']}" for a in articles]
        )

        prompt = f"""Summarize these {topic} articles into 2-3 sentences for a daily digest:

{articles_text}

Focus on main themes and key developments. Be concise and informative."""

        summary = self._call_llm(prompt)
        return summary.strip()

    async def _save_result(self, result: Dict[str, Any], output_path: str):
        """Save summary."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# AI/ML Daily Digest - Summary\n\n")
            f.write(f"**Total Articles:** {result['total_articles']}\n\n")

            for topic, summary in result["summaries"].items():
                articles_count = len(result["topics"][topic])
                f.write(f"## {topic} ({articles_count} articles)\n\n")
                f.write(f"{summary}\n\n")
                f.write("---\n\n")

        print(f"💾 Saved summary to {output_path}")
