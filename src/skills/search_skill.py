"""Reusable search skill using MCP."""

import asyncio
import json
import sys
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class SearchSkill:
    """
    Reusable skill for searching articles.

    Uses MCP database server to search.
    Demonstrates skill pattern: higher-level abstraction over tools.
    """

    def __init__(self):
        self.server_params = StdioServerParameters(
            command=sys.executable, args=["-m", "src.mcp.database_server"]
        )

    async def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for articles.

        Args:
            query: Search query
            limit: Max results

        Returns:
            Dict with results and metadata
        """
        print(f"🔍 SearchSkill: Searching for '{query}'...")

        try:
            # Connect to MCP server
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call search tool
                    result = await session.call_tool(
                        "search_articles", {"query": query, "limit": limit}
                    )

                    # Parse result
                    data = json.loads(result.content[0].text)

                    print(f"   Found {data['total']} matches")

                    return {
                        "success": True,
                        "query": query,
                        "total": data["total"],
                        "articles": data["articles"],
                    }

        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            return {"success": False, "query": query, "error": str(e), "articles": []}


# Test it
async def test_search_skill():
    """Test search skill."""
    skill = SearchSkill()

    result = await skill.search("machine learning", limit=5)

    print("\n✅ SearchSkill tested")
    print(f"   Success: {result['success']}")
    print(f"   Total: {result['total']}")
    print(f"   Articles: {len(result['articles'])}")

    if result["articles"]:
        print("\n   First result:")
        print(f"   - {result['articles'][0]['title']}")


if __name__ == "__main__":
    asyncio.run(test_search_skill())
