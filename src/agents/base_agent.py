"""Base class for AI agents."""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from litellm import completion


class BaseAgent(ABC):
    """
    Base class for all AI agents.

    Implements Template Method pattern:
    - execute() orchestrates the workflow
    - Subclasses implement specific steps
    """

    def __init__(
        self,
        model: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
    ):
        self.model = model or os.getenv("LITELLM_MODEL")
        if not self.model:
            raise ValueError(
                "No model configured. Set LITELLM_MODEL in .env "
                "or pass `model=` to the agent constructor."
            )
        self.tools = tools or []
        self.tool_functions: Dict[str, Callable] = {}

    async def execute(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """
        Execute agent workflow (Template Method).

        Steps:
        1. Load input context
        2. Process with LLM
        3. Save results

        Args:
            input_path: Path to input markdown file
            output_path: Path to save output

        Returns:
            Result metadata
        """
        print(f"\n🤖 {self.__class__.__name__} starting...")

        # Step 1: Load
        context = await self._load_context(input_path)

        # Step 2: Process
        result = await self._process(context)

        # Step 3: Save
        await self._save_result(result, output_path)

        print(f"✅ {self.__class__.__name__} complete")

        return {
            "input_path": input_path,
            "output_path": output_path,
            "success": True,
        }

    @abstractmethod
    async def _load_context(self, input_path: str) -> Dict[str, Any]:
        """Load input context. Subclasses implement how to read their input."""
        raise NotImplementedError

    @abstractmethod
    async def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context with LLM. Subclasses implement their specific logic."""
        raise NotImplementedError

    @abstractmethod
    async def _save_result(self, result: Dict[str, Any], output_path: str):
        """Save processing result. Subclasses implement how to save their output."""
        raise NotImplementedError

    def _call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Call the configured LLM via LiteLLM.

        Helper method for subclasses.

        Args:
            prompt: User prompt.
            system: Optional system prompt.

        Returns:
            LLM response text.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = completion(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            raise

    def register_tool_function(self, name: str, function: Callable) -> None:
        """Register the actual Python function backing a tool schema."""
        self.tool_functions[name] = function

    def _call_llm_with_tools(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Call the LLM with tool support, looping until the model returns text.

        Tool-call protocol:
          1. Send prompt + tool schemas.
          2. If response contains tool_calls, execute each tool locally.
          3. Append the assistant message and each tool result back into messages.
          4. Call the model again.
          5. Repeat until the model returns plain text.
        """
        messages: List[Dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Hard cap on tool-call rounds — protects against infinite loops.
        for _ in range(10):
            response = completion(
                model=self.model,
                messages=messages,
                tools=self.tools or None,
            )
            msg = response.choices[0].message

            # No tool calls -> we're done.
            if not getattr(msg, "tool_calls", None):
                return msg.content

            # Record the assistant turn (must come before tool results).
            messages.append(msg.model_dump())

            # Execute each tool call and append its result.
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments or "{}")
                print(f"   🔧 Tool call: {name}({args})")

                if name not in self.tool_functions:
                    raise ValueError(f"Tool {name!r} not registered")

                result = self.tool_functions[name](**args)
                print(f"   📊 Tool result: {result}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": json.dumps(result),
                    }
                )

        raise RuntimeError("Tool-call loop exceeded 10 rounds — model is stuck.")
