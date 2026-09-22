# Milestone 4: MCP-Powered Multi-Agent Pipeline

**⏰ Time Commitment:** 5-7 evenings (10-14 hours)  
**When:** Week 4, Days 16-22  
**Prerequisites:** Milestone 3 complete and PR merged  
**Checkpoint:** ✓ Checkpoint 4 (after completion)  
**Next Milestone:** [Milestone 5: Evaluation & Documentation](milestone-5-evaluation.md)

---

## 🎯 Learning Objectives

By the end of this week, you will:
- Understand Model Context Protocol (MCP)
- Build a production MCP server (Database server)
- Create a reusable agent skill (SearchSkill)
- Build 3-agent pipeline (Filter → Summarize → Write)
- Integrate agents with MCP tools
- Understand multi-agent orchestration
- Build complete tool-enhanced AI system

**This is the biggest milestone - everything comes together!** 🚀

---

## 📚 Week 4 Overview

```
Week 4: MCP & Multi-Agent Pipeline
├── Evening 16 (Mon): MCP Protocol Basics
├── Evening 17 (Tue): Database MCP Server (Part 1)
├── Evening 18 (Wed): Database MCP Server (Part 2)
├── Evening 19 (Thu): SearchSkill + MCP Client
├── Evening 20 (Fri): SummarizerAgent + WriterAgent
├── Evening 21 (Mon): Complete Pipeline Integration
└── Evening 22 (Tue): Testing + PR

Total: 10-14 hours over 5-7 evenings
```

---

## 📖 Required Reading (Before Evening 16)

**Read these first (1 hour total):**

1. **MCP Specification Overview (20 min)**
   - https://spec.modelcontextprotocol.io/
   - Read: Introduction, Core Concepts

2. **MCP Python SDK (20 min)**
   - https://github.com/modelcontextprotocol/python-sdk
   - Read: README and basic example

3. **Tool Design Principles (20 min)**
   - Think about: What makes a good tool?
   - Single purpose, clear inputs/outputs, error handling

**Done reading?** Start Evening 16! 🚀

---

## 🌙 Evening 16: MCP Protocol Basics

**⏰ Time:** 2 hours  
**Goal:** Understand MCP and build hello world server

### **Timeline:**

```
7:30 PM - Start
├── 7:30-8:00 PM (30 min) - Install MCP SDK
├── 8:00-8:45 PM (45 min) - Build hello world MCP server
└── 8:45-9:30 PM (45 min) - Test with MCP client
9:30 PM - Done!
```

---

### **Step 1: Install MCP SDK (15 min)**

```bash
# Install MCP
pip install mcp

# Verify
python -c "import mcp; print('✅ MCP installed')"
```

---

### **Step 2: Understand MCP Basics (15 min)**

**Key Concepts:**

```python
# MCP Server provides TOOLS to clients
# Tools are functions that clients can call

# Server = Tool Provider
# Client = Tool Consumer (your agents!)

# Communication via:
# - stdio (standard input/output) - easiest for local
# - HTTP - for remote servers
# - WebSocket - for persistent connections
```

**MCP Flow:**

```
1. Client connects to Server
2. Client asks: "What tools do you have?"
3. Server responds: "I have tool X, Y, Z"
4. Client: "Call tool X with these arguments"
5. Server: "Here's the result"
```

---

### **Step 3: Build Hello World MCP Server (45 min)**

**File:** `src/mcp/hello_server.py`

```python
"""Hello World MCP server."""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


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
            input_schema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of person to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="add",
            description="Add two numbers",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute a tool.
    
    This is called when client says "call tool X".
    """
    if name == "greet":
        person_name = arguments["name"]
        greeting = f"Hello, {person_name}! 👋"
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
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

**Test your server:**

```bash
# Run server (it will wait for input)
python src/mcp/hello_server.py

# In another terminal, you can test with MCP inspector
# (We'll build a proper client next)
```

---

### **Step 4: Build Simple MCP Client (45 min)**

**File:** `src/mcp/simple_client.py`

```python
"""Simple MCP client for testing."""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_hello_server():
    """Test hello world MCP server."""
    print("🔌 Connecting to hello-world server...")
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp/hello_server.py"]
    )
    
    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Call greet tool
            print(f"\n🔧 Calling 'greet' tool...")
            result = await session.call_tool("greet", {"name": "Alice"})
            print(f"   Result: {result.content[0].text}")
            
            # Call add tool
            print(f"\n🔧 Calling 'add' tool...")
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"   Result: {result.content[0].text}")
            
            print("\n✅ MCP communication working!")


if __name__ == "__main__":
    asyncio.run(test_hello_server())
```

**Test it:**

```bash
python src/mcp/simple_client.py

# Should connect to server and call tools!
```

---

### **Evening 16 Deliverable:**

✅ MCP SDK installed  
✅ Hello world server working  
✅ MCP client connecting  
✅ Tool calling functional  
✅ Understanding of MCP protocol  

**Time used:** 2 hours

---

## 🌙 Evening 17-18: Database MCP Server

**⏰ Time:** 3-4 hours (split over 2 evenings)  
**Goal:** Build production MCP server for database access

### **Evening 17 Timeline (2 hours):**

```
7:30 PM - Start
├── 7:30-8:15 PM (45 min) - Create SQLite database
├── 8:15-9:00 PM (45 min) - Implement query_articles tool
└── 9:00-9:30 PM (30 min) - Test queries
9:30 PM - Done!
```

---

### **Step 1: Create SQLite Database (45 min)**

**File:** `src/database/db_manager.py`

```python
"""SQLite database manager for articles."""
import sqlite3
import aiosqlite
from pathlib import Path
from typing import List, Dict
from datetime import datetime


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
        
        print(f"✅ Database initialized: {self.db_path}")
    
    async def insert_article(self, article: Dict):
        """Insert article into database."""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("""
                    INSERT INTO articles 
                    (title, url, source, published_at, summary, score, relevance_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    article['title'],
                    article['url'],
                    article['source'],
                    article['published_at'],
                    article.get('summary', ''),
                    article.get('score', 0),
                    article.get('relevance_score', 0)
                ))
                await db.commit()
            except sqlite3.IntegrityError:
                # URL already exists, skip
                pass
    
    async def query_articles(
        self,
        source: str = None,
        limit: int = 50
    ) -> List[Dict]:
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
    await db.insert_article({
        'title': 'Test Article',
        'url': 'https://test.com/article1',
        'source': 'test',
        'published_at': datetime.now().isoformat(),
        'summary': 'Test summary'
    })
    
    # Query
    articles = await db.query_articles(limit=10)
    print(f"✅ Found {len(articles)} articles")
    for article in articles:
        print(f"  - {article['title']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_db())
```

**Test database:**

```bash
python src/database/db_manager.py

# Creates database and tests queries
```

---

### **Step 2: Implement Database MCP Server (45 min)**

**File:** `src/mcp/database_server.py`

```python
"""Database MCP server - provides tools to query article database."""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from src.database.db_manager import DatabaseManager
import json


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
            input_schema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Filter by source (optional, e.g., 'hackernews', 'rss')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of articles to return",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="search_articles",
            description="Search articles by keyword in title or summary",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches in title and summary)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_sources",
            description="Get list of all available sources in database",
            input_schema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute database tool."""
    if not db_manager:
        await init_db()
    
    if name == "query_articles":
        articles = await db_manager.query_articles(
            source=arguments.get("source"),
            limit=arguments.get("limit", 50)
        )
        
        result = {
            "total": len(articles),
            "articles": articles[:10]  # Return first 10 full, rest just count
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "search_articles":
        # Simple search implementation
        query = arguments["query"].lower()
        limit = arguments.get("limit", 20)
        
        # Get all articles and filter
        all_articles = await db_manager.query_articles(limit=1000)
        
        matches = [
            article for article in all_articles
            if query in article['title'].lower() or 
               query in article.get('summary', '').lower()
        ]
        
        result = {
            "total": len(matches),
            "query": query,
            "articles": matches[:limit]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_sources":
        # Get unique sources
        articles = await db_manager.query_articles(limit=1000)
        sources = list(set(a['source'] for a in articles))
        
        result = {
            "sources": sources,
            "total": len(sources)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run database MCP server."""
    await init_db()
    print("🗄️  Database MCP Server starting...")
    print("   Tools: query_articles, search_articles, get_sources")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

---

### **Step 3: Test Database Server (30 min)**

**File:** `test_db_server.py`

```python
"""Test database MCP server."""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_database_server():
    """Test database MCP server."""
    print("🔌 Connecting to database server...")
    
    server_params = StdioServerParameters(
        command="python",
        args=["src/mcp/database_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"\n📋 Database tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Get sources
            print(f"\n🔧 Getting sources...")
            result = await session.call_tool("get_sources", {})
            print(f"   {result.content[0].text[:200]}")
            
            # Query articles
            print(f"\n🔧 Querying articles...")
            result = await session.call_tool("query_articles", {"limit": 5})
            print(f"   {result.content[0].text[:300]}")
            
            # Search
            print(f"\n🔧 Searching for 'AI'...")
            result = await session.call_tool("search_articles", {
                "query": "AI",
                "limit": 3
            })
            print(f"   {result.content[0].text[:300]}")
            
            print("\n✅ Database MCP server working!")


if __name__ == "__main__":
    asyncio.run(test_database_server())
```

**But first, populate database with your articles:**

```python
# populate_db.py
import asyncio
from src.database.db_manager import DatabaseManager
from pathlib import Path
import re
from datetime import datetime


async def populate_from_markdown():
    """Populate database from markdown files."""
    db = DatabaseManager()
    await db.initialize()
    
    # Read articles from markdown
    articles_dir = Path("data/articles")
    
    for md_file in articles_dir.glob("*.md"):
        print(f"Reading {md_file.name}...")
        content = md_file.read_text()
        
        # Simple parsing
        sections = content.split('---')
        
        for section in sections:
            if '##' not in section:
                continue
            
            # Extract title
            title_match = re.search(r'## (.+)', section)
            if not title_match:
                continue
            title = title_match.group(1).strip()
            
            # Extract URL
            url_match = re.search(r'\*\*URL:\*\* (.+)', section)
            if not url_match:
                continue
            url = url_match.group(1).strip()
            
            # Extract source
            source_match = re.search(r'\*\*Source:\*\* (.+)', section)
            source = source_match.group(1).strip() if source_match else 'unknown'
            
            # Extract summary
            lines = [l for l in section.split('\n') if l.strip() and not l.startswith('**')]
            summary = lines[-1] if lines else ""
            
            # Insert
            await db.insert_article({
                'title': title,
                'url': url,
                'source': source,
                'published_at': datetime.now().isoformat(),
                'summary': summary
            })
    
    # Check count
    articles = await db.query_articles(limit=1000)
    print(f"\n✅ Database populated with {len(articles)} articles")


if __name__ == "__main__":
    asyncio.run(populate_from_markdown())
```

**Run it:**

```bash
# First, populate database
python populate_db.py

# Then test server
python test_db_server.py

# Should work! ✅
```

---

### **Evening 17 Deliverable:**

✅ SQLite database created  
✅ Database MCP server implemented  
✅ 3 tools working (query, search, get_sources)  
✅ Database populated with articles  
✅ Server tested  

**Time used:** 2 hours

---

### **Evening 18 Timeline (1.5-2 hours):**

```
7:30 PM - Start
├── 7:30-8:15 PM (45 min) - Create SearchSkill
├── 8:15-9:00 PM (45 min) - Build MCP client wrapper
└── 9:00-9:30 PM (30 min) - Test skill with MCP
9:30 PM - Done!
```

---

### **Step 4: Create SearchSkill (45 min)**

**File:** `src/skills/search_skill.py`

```python
"""Reusable search skill using MCP."""
from typing import List, Dict, Any
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json


class SearchSkill:
    """
    Reusable skill for searching articles.
    
    Uses MCP database server to search.
    Demonstrates skill pattern: higher-level abstraction over tools.
    """
    
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["src/mcp/database_server.py"]
        )
    
    async def search(
        self,
        query: str,
        limit: int = 10
    ) -> Dict[str, Any]:
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
                        "search_articles",
                        {"query": query, "limit": limit}
                    )
                    
                    # Parse result
                    data = json.loads(result.content[0].text)
                    
                    print(f"   Found {data['total']} matches")
                    
                    return {
                        'success': True,
                        'query': query,
                        'total': data['total'],
                        'articles': data['articles']
                    }
        
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'articles': []
            }


# Test it
async def test_search_skill():
    """Test search skill."""
    skill = SearchSkill()
    
    result = await skill.search("machine learning", limit=5)
    
    print(f"\n✅ SearchSkill tested")
    print(f"   Success: {result['success']}")
    print(f"   Total: {result['total']}")
    print(f"   Articles: {len(result['articles'])}")
    
    if result['articles']:
        print(f"\n   First result:")
        print(f"   - {result['articles'][0]['title']}")


if __name__ == "__main__":
    asyncio.run(test_search_skill())
```

**Test it:**

```bash
python src/skills/search_skill.py

# Should search database!
```

---

### **Evening 18 Deliverable:**

✅ SearchSkill implemented  
✅ MCP client integration  
✅ Skill pattern demonstrated  
✅ Tested and working  

**Time used:** 1.5-2 hours

---

## 🌙 Evening 19-20: Multi-Agent Pipeline

**⏰ Time:** 3-4 hours (split over 2 evenings)  
**Goal:** Build SummarizerAgent and WriterAgent

### **Evening 19: SummarizerAgent (2 hours)**

**File:** `src/agents/summarizer_agent.py`

```python
"""Agent that summarizes filtered articles."""
from typing import Dict, Any
from pathlib import Path
from src.agents.base_agent import BaseAgent
from src.skills.search_skill import SearchSkill
import json
import re


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
        
        content = Path(input_path).read_text()
        
        # Parse articles
        articles = self._parse_markdown(content)
        
        print(f"   Found {len(articles)} filtered articles")
        return {"articles": articles}
    
    def _parse_markdown(self, content: str) -> list[Dict]:
        """Parse markdown to extract articles."""
        articles = []
        sections = content.split('---')
        
        for section in sections:
            if '##' not in section:
                continue
            
            title_match = re.search(r'## (.+)', section)
            if not title_match:
                continue
            
            title = title_match.group(1).strip()
            
            # Extract relevance score
            score_match = re.search(r'\*\*Relevance Score:\*\* (\d+)', section)
            relevance = int(score_match.group(1)) if score_match else 0
            
            # Extract reasoning
            reason_match = re.search(r'\*\*Reasoning:\*\* (.+)', section)
            reasoning = reason_match.group(1).strip() if reason_match else ""
            
            # Extract topics
            topics_match = re.search(r'\*\*Key Topics:\*\* (.+)', section)
            topics = topics_match.group(1).strip() if topics_match else ""
            
            articles.append({
                'title': title,
                'relevance': relevance,
                'reasoning': reasoning,
                'topics': topics
            })
        
        return articles
    
    async def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize articles."""
        articles = context['articles']
        
        print(f"📝 Summarizing {len(articles)} articles...")
        
        # Group by topic
        topics = {}
        for article in articles:
            topic = article['topics'].split(',')[0] if article['topics'] else 'Other'
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
            'topics': topics,
            'summaries': summaries,
            'total_articles': len(articles)
        }
    
    async def _summarize_topic(self, topic: str, articles: list[Dict]) -> str:
        """Generate summary for a topic."""
        # Create prompt
        articles_text = "\n".join([
            f"- {a['title']}: {a['reasoning']}"
            for a in articles
        ])
        
        prompt = f"""Summarize these {topic} articles into 2-3 sentences for a daily digest:

{articles_text}

Focus on main themes and key developments. Be concise and informative."""

        summary = self._call_llm(prompt)
        return summary.strip()
    
    async def _save_result(self, result: Dict[str, Any], output_path: str):
        """Save summary."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("# AI/ML Daily Digest - Summary\n\n")
            f.write(f"**Total Articles:** {result['total_articles']}\n\n")
            
            for topic, summary in result['summaries'].items():
                articles_count = len(result['topics'][topic])
                f.write(f"## {topic} ({articles_count} articles)\n\n")
                f.write(f"{summary}\n\n")
                f.write("---\n\n")
        
        print(f"💾 Saved summary to {output_path}")
```

**Test it:**

```python
# test_summarizer.py
import asyncio
from src.agents.summarizer_agent import SummarizerAgent


async def test():
    agent = SummarizerAgent()
    await agent.execute(
        input_path="data/context/filtered_articles.md",
        output_path="data/context/summary.md"
    )


asyncio.run(test())
```

---

### **Evening 20: WriterAgent (2 hours)**

**File:** `src/agents/writer_agent.py`

```python
"""Agent that writes newsletter from summary."""
from typing import Dict, Any
from pathlib import Path
from src.agents.base_agent import BaseAgent
from datetime import datetime


class WriterAgent(BaseAgent):
    """
    Writes newsletter from summary.
    
    Final step in pipeline.
    """
    
    async def _load_context(self, input_path: str) -> Dict[str, Any]:
        """Load summary."""
        print(f"📖 Loading summary from {input_path}")
        content = Path(input_path).read_text()
        return {"summary": content}
    
    async def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Write newsletter."""
        summary = context['summary']
        
        print(f"✍️  Writing newsletter...")
        
        prompt = f"""You are writing a daily AI/ML newsletter.

Here's the summary of today's articles:

{summary}

Write an engaging newsletter with:
1. Catchy introduction (2-3 sentences)
2. Main content organized by topic (keep the summaries, add context)
3. Brief conclusion

Use a professional but friendly tone. Include emoji sparingly."""

        newsletter = self._call_llm(prompt)
        
        return {
            'newsletter': newsletter,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    
    async def _save_result(self, result: Dict[str, Any], output_path: str):
        """Save newsletter."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(f"# AI/ML Daily Newsletter - {result['date']}\n\n")
            f.write(result['newsletter'])
            f.write("\n\n---\n\n")
            f.write(f"*Generated by AI Agent Pipeline*\n")
        
        print(f"💾 Newsletter saved to {output_path}")
```

---

## 🌙 Evening 21: Complete Pipeline Integration

**⏰ Time:** 2 hours  
**Goal:** Connect all agents into complete pipeline

**File:** `src/complete_pipeline.py`

```python
"""Complete multi-agent pipeline with MCP."""
import asyncio
from pathlib import Path
from src.orchestrator import FetchOrchestrator
from src.agents.news_filter_agent import NewsFilterAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.agents.writer_agent import WriterAgent
from src.database.db_manager import DatabaseManager


async def run_complete_pipeline():
    """
    Run complete pipeline:
    1. Fetch articles (Milestone 1)
    2. Save to database
    3. Filter with AI (Milestone 3)
    4. Summarize (Milestone 4)
    5. Write newsletter (Milestone 4)
    """
    print("=" * 70)
    print("  Complete AI Agent Pipeline with MCP")
    print("=" * 70)
    
    # Step 1: Fetch
    print("\n📰 Step 1: Fetching articles from sources...")
    orchestrator = FetchOrchestrator()
    articles = await orchestrator.fetch_all()
    fetch_output = Path("data/articles/all_articles.md")
    print(f"✅ Fetched {len(articles)} articles → {fetch_output}")
    
    # Step 2: Save to database
    print("\n💾 Step 2: Saving to database...")
    db = DatabaseManager()
    await db.initialize()
    for article in articles:
        await db.insert_article({
            'title': article.title,
            'url': article.url,
            'source': article.source,
            'published_at': article.published_at.isoformat(),
            'summary': article.summary,
            'score': getattr(article, 'score', 0)
        })
    db_articles = await db.query_articles(limit=1000)
    print(f"✅ Database has {len(db_articles)} articles")
    
    # Step 3: Filter
    print("\n🤖 Step 3: Filtering with AI agent...")
    filter_agent = NewsFilterAgent()
    filter_output = Path("data/context/filtered_articles.md")
    await filter_agent.execute(
        input_path=str(fetch_output),
        output_path=str(filter_output)
    )
    print(f"✅ Filtered articles → {filter_output}")
    
    # Step 4: Summarize
    print("\n📝 Step 4: Summarizing with AI agent...")
    summarizer = SummarizerAgent()
    summary_output = Path("data/context/summary.md")
    await summarizer.execute(
        input_path=str(filter_output),
        output_path=str(summary_output)
    )
    print(f"✅ Summary → {summary_output}")
    
    # Step 5: Write
    print("\n✍️  Step 5: Writing newsletter...")
    writer = WriterAgent()
    newsletter_output = Path("data/output/newsletter.md")
    await writer.execute(
        input_path=str(summary_output),
        output_path=str(newsletter_output)
    )
    print(f"✅ Newsletter → {newsletter_output}")
    
    print("\n" + "=" * 70)
    print("🎉 Complete Pipeline Success!")
    print("=" * 70)
    print(f"\n📊 Pipeline Summary:")
    print(f"   1. Fetched: {len(articles)} articles")
    print(f"   2. Database: {len(db_articles)} total articles")
    print(f"   3. Filtered: {filter_output}")
    print(f"   4. Summarized: {summary_output}")
    print(f"   5. Newsletter: {newsletter_output}")
    print(f"\n📖 Read your newsletter:")
    print(f"   cat {newsletter_output}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_complete_pipeline())
```

**Run it:**

```bash
python src/complete_pipeline.py

# Complete pipeline! 🎉
```

---

## 🌙 Evening 22: Testing + PR

**⏰ Time:** 1-2 hours  
**Goal:** Test and submit PR

```bash
# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Create PR
git add .
git commit -m "feat: MCP-powered multi-agent pipeline"
git push origin feature/milestone-4-mcp-pipeline
```

**PR Description:** *(see separate section below)*

---

## 🎉 Milestone 4 Complete!

### **What You Accomplished:**

✅ Built production MCP server (Database)  
✅ Created SearchSkill pattern  
✅ Built 3-agent pipeline (Filter → Summarize → Write)  
✅ Integrated MCP tools with agents  
✅ Complete working system!  

### **Skills Gained (25 skills):**

1-6. MCP protocol, server/client implementation  
7-9. Database tools (query, search, sources)  
10-12. Skill abstraction pattern  
13-15. Multi-agent orchestration  
16-18. Pipeline design  
19-21. Agent coordination  
22-25. Production integration  

---

## ➡️ Next Steps

Proceed to [Milestone 5: Evaluation & Documentation](milestone-5-evaluation.md)

**Time:** 2-3 evenings (4-6 hours)

---

**Milestone 4 Complete** ✅  
**Time Spent:** 10-14 hours over 5-7 evenings  
**Next:** Milestone 5 (Week 5)
