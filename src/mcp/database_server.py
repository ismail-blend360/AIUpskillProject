"""Database MCP server - provides tools to query article database."""

import asyncio
import json
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from src.database.db_manager import DatabaseManager

# Create server
server = Server("database-server")

# Database manager
db_manager = None


async def init_db():
    """Initialize database."""
    global db_manager
    db_manager = DatabaseManager()
    await db_manager.initialize()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List database tools."""
    return [
        Tool(
            name="query_articles",
            description="Query articles from database with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Filter by source (optional, e.g., 'hackernews', 'rss')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of articles to return",
                        "default": 50,
                    },
                },
            },
        ),
        Tool(
            name="search_articles",
            description="Search articles by keyword in title or summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches in title and summary)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results",
                        "default": 20,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_sources",
            description="Get list of all available sources in database",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute database tool."""
    if not db_manager:
        await init_db()

    if name == "query_articles":
        articles = await db_manager.query_articles(
            source=arguments.get("source"), limit=arguments.get("limit", 50)
        )

        result = {
            "total": len(articles),
            "articles": articles[:10],  # Return first 10 full, rest just count
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "search_articles":
        # Simple search implementation
        query = arguments["query"].lower()
        limit = arguments.get("limit", 20)

        # Get all articles and filter
        all_articles = await db_manager.query_articles(limit=1000)

        matches = [
            article
            for article in all_articles
            if query in article["title"].lower()
            or query in article.get("summary", "").lower()
        ]

        result = {"total": len(matches), "query": query, "articles": matches[:limit]}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_sources":
        # Get unique sources
        articles = await db_manager.query_articles(limit=1000)
        sources = list(set(a["source"] for a in articles))

        result = {"sources": sources, "total": len(sources)}

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    else:
        raise ValueError(f"Unknown tool: {name}")


# async def main():
#     """Run database MCP server."""
#     await init_db()
#     print("Database MCP Server starting...", file=sys.stderr)
#     print("Tools: query_articles, search_articles, get_sources", file=sys.stderr)

#     async with stdio_server() as (read_stream, write_stream):
#         await server.run(
#             read_stream,
#             write_stream,
#             server.create_initialization_options()
#         )


async def main():
    """Run database MCP server."""
    try:
        await init_db()

        print("Database MCP Server starting...", file=sys.stderr)
        print("Tools: query_articles, search_articles, get_sources", file=sys.stderr)

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    except Exception as e:
        import traceback

        print(f"SERVER ERROR: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


if __name__ == "__main__":
    asyncio.run(main())
