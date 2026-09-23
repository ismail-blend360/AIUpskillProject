# test_summarizer.py
import asyncio

from src.agents.summarizer_agent import SummarizerAgent


async def test():
    agent = SummarizerAgent()
    await agent.execute(
        input_path="data/context/filtered_articles.md",
        output_path="data/context/summary.md",
    )


asyncio.run(test())
