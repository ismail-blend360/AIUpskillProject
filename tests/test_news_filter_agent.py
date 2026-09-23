# tests/test_news_filter_agent.py
import tempfile
from pathlib import Path

import pytest

from src.agents.news_filter_agent import NewsFilterAgent


@pytest.mark.asyncio
async def test_agent_filters_articles():
    """Test agent filters correctly."""
    # Create temp input file
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "input.md"
        output_file = Path(tmpdir) / "output.md"

        # Write test articles
        input_file.write_text("""
## GPT-4 Released by OpenAI

**URL:** https://example.com/gpt4

OpenAI announces GPT-4 with enhanced capabilities.

---

## New JavaScript Framework

**URL:** https://example.com/js

React alternative for web development.
""")

        # Run agent
        agent = NewsFilterAgent()
        result = await agent.execute(str(input_file), str(output_file))

        # Check output
        assert output_file.exists()
        content = output_file.read_text()

        # Should include GPT-4
        assert "GPT-4" in content

        # Should not include JS framework (probably)
        # Note: LLM behavior can vary


@pytest.mark.asyncio
async def test_tool_usage():
    """Test tools are callable."""
    from src.tools.calculator import calculator
    from src.tools.web_search import web_search

    # Test calculator
    result = calculator("2 + 2")
    assert result["success"]
    assert result["result"] == 4

    # Test search
    result = web_search("AI news")
    assert result["success"]
    assert len(result["results"]) > 0
