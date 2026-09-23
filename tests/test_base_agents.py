# Test base agent
from src.agents.base_agent import BaseAgent


class TestAgent(BaseAgent):
    async def _load_context(self, input_path):
        return {"test": "data"}

    async def _process(self, context):
        response = self._call_llm("Say hello")
        return {"response": response}

    async def _save_result(self, result, output_path):
        print(f"Would save: {result}")


# Test it
import asyncio

agent = TestAgent()
asyncio.run(agent.execute("input.md", "output.md"))
