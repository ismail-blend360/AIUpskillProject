# Architecture Overview

**Read time:** 20 minutes

This document describes what you're building, how the pieces fit together, and
why we chose this shape. Read it once at the start of Milestone 0, then refer
back when you need orientation.

---

## System Overview

You're building a small **AI-powered news pipeline** that runs entirely on your
laptop. It fetches articles from public sources, filters them with an LLM,
summarizes the ones worth keeping, and writes a daily digest. Along the way
you learn async Python, SOLID design, AI agents, the Model Context Protocol
(MCP), and evaluation.

The project is deliberately small. Two news sources, three agents, one MCP
server, one persisted database. You build one of each really well rather than
many of each shallowly.

---

## Data Flow

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│  Hacker News   │    │  RSS (Verge)   │    │  GitHub        │
│  fetcher       │    │  fetcher       │    │  Trending      │
└───────┬────────┘    └───────┬────────┘    │  fetcher (M2)  │
        │                     │             └───────┬────────┘
        └─────────┬───────────┴─────────────────────┘
                  ▼
         ┌─────────────────┐
         │   Orchestrator  │   Concurrent fetch, rate-limited,
         │     (M1)        │   produces a list of Article objects
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │  MarkdownStorage│   Writes each article as a .md file
         │     (M1)        │   in data/articles/
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │ NewsFilterAgent │   LLM call (via LiteLLM) decides
         │     (M3)        │   relevant / not, with a score
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │SummarizerAgent  │   Reduces each kept article to
         │     (M4)        │   3–5 bullet points
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │   WriterAgent   │   Composes the daily digest as
         │     (M4)        │   one markdown document
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │ MCP Database    │   Persists articles + summaries to
         │ Server (M4)     │   SQLite, exposed as MCP tools
         └─────────────────┘
```

**Articles flow as markdown files between stages.** That's deliberate. Markdown
is human-readable so you can debug the pipeline by opening a file in your
editor, git-friendly so you can diff what the agents produced across runs, and
it's the natural format for LLM context windows. The MCP database server in
Milestone 4 layers persistent structured storage *underneath* the markdown,
not as a replacement for it.

---

## Tech Stack

**Language: Python 3.11+.** Async features needed for `aiohttp` and
`asyncio.gather`; type hints used throughout for self-documenting code.

**HTTP: `aiohttp`.** Concurrent fetches without threads. Milestone 1 teaches
this from scratch.

**LLM access: LiteLLM.** A thin wrapper over Anthropic / OpenAI / Gemini /
others that gives you one consistent API. You set `LITELLM_MODEL` in `.env` to
the model you want and the rest of the code stays unchanged. Default is
`claude-haiku-4-5-20251001` — cheap, fast, and Anthropic's $5 trial credit
covers the whole curriculum.

**Tool integration: Model Context Protocol (MCP).** An open protocol for
exposing tools (functions an LLM can call) over a standard interface. You build
one MCP server in Milestone 4 and connect your agents to it.

**Database: SQLite.** Local file, no server. The MCP database server you build
in Milestone 4 sits on top of it.

**Testing: pytest + pytest-asyncio.** Tests live next to the code they exercise
and run on every PR.

**Code quality: ruff.** Formats and lints in one step, replacing the older
black + isort + pylint trio.

---

## Week-by-week preview

**Week 1 — Foundations (M0, M1).** Set up the environment. Build the async
news fetcher: a Hacker News fetcher, an RSS fetcher, an orchestrator that runs
them concurrently with rate limiting, and markdown storage. End of week: you
can pull dozens of articles from two sources in seconds.

**Week 2 — SOLID Refactoring (M2).** Walk through all five SOLID principles
and refactor your Week 1 code as you go. The acid test is adding a third
fetcher (GitHub Trending) without modifying any existing class — that proves
Open/Closed. You'll also apply the Factory, Strategy, and Template Method
patterns. End of week: your code is professional-grade.

**Week 3 — First AI Agent (M3).** Add `NewsFilterAgent`: an LLM call (via
LiteLLM) that decides whether each article is relevant, with a score and a
reason. You'll learn prompt engineering, structured outputs, function calling,
and how to handle LLM errors gracefully.

**Week 4 — MCP + Multi-Agent (M4).** Build a Database MCP server that exposes
three tools (save, search, get). Connect it to the agents you already have,
then add two more — `SummarizerAgent` and `WriterAgent` — to form a three-agent
pipeline. End of week: you have a working multi-agent system orchestrated
through MCP.

**Week 5 — Evaluation (M5).** Hand-label a small golden dataset, write an
evaluator that calculates accuracy / precision / recall / F1 for the filter,
and write the project's README and architecture docs. End of week: portfolio-
quality, production-ready.

---

## Why this shape

A few decisions worth understanding before you start:

**Everything runs locally.** No cloud, no deployment, no Docker. The whole
project should run on your laptop in under a minute end-to-end. This keeps the
feedback loop tight while you're learning.

**Markdown as the interchange format.** When an agent's output is a `.md` file,
you can read it. When agents pass messages through markdown, you can debug the
pipeline by opening files. This costs a small amount of parsing overhead and
buys huge legibility.

**One real example of each pattern.** You build one fetcher pattern (then
extend it twice), one agent pattern (then extend it twice), one MCP server.
The goal is depth over breadth — you finish the project understanding *why*
each pattern exists, not just *that* it exists.

**Progressive complexity.** Each milestone depends on the previous one. By
Week 4 you're connecting code you wrote in Week 1 to agents you wrote in Week
3 through an MCP server you wrote in Week 4. The system stays small, but the
moving parts compound.
