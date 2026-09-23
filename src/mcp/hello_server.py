"""Hello World MCP server."""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Create server
server = Server("hello-world")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available tools.

    This is called when client asks "what tools do you have?"
    """
    return [
        Tool(
            name="greet",
            description="Greet someone by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of person to greet"}
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute a tool.

    This is called when client says "call tool X".
    """
    if name == "greet":
        person_name = arguments["name"]
        greeting = f"Hello, {person_name}!"
        return [TextContent(type="text", text=greeting)]

    elif name == "add":
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [TextContent(type="text", text=f"{a} + {b} = {result}")]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the server."""
    # Run with stdio transport (for local use)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
