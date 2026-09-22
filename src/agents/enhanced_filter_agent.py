"""News filter agent with tool use."""
import json
from src.agents.news_filter_agent import NewsFilterAgent
from src.agents.base_agent import BaseAgent
from src.tools.calculator import calculator, CALCULATOR_SCHEMA
from src.tools.web_search import web_search, WEB_SEARCH_SCHEMA
from typing import Dict

class EnhancedFilterAgent(NewsFilterAgent):
    """
    Filter agent that can use tools.

    Extends NewsFilterAgent with calculator and search.
    """

    def __init__(self):
        # Pass tools through to BaseAgent so they're sent on every LLM call.
        super().__init__(tools=[CALCULATOR_SCHEMA, WEB_SEARCH_SCHEMA])

        # Register the actual Python functions backing each tool schema.
        self.register_tool_function("calculator", calculator)
        self.register_tool_function("web_search", web_search)

    def _judge_relevance(self, article: Dict) -> Dict:
        """
        Judge relevance with tool access.

        LLM can now call calculator or search if needed.
        """
        prompt = f"""You are an AI/ML news analyst with access to tools.

                    Article:
                    Title: {article['title']}
                    Summary: {article['summary']}

                    Judge if this is AI/ML relevant. You can use:
                    - calculator: for any math calculations
                    - web_search: to verify claims or get context

                    Output JSON:
                    {{
                    "relevant": true/false,
                    "relevance_score": 1-10,
                    "reasoning": "explanation (mention if you used tools)",
                    "key_topics": ["topic1", "topic2"]
                    }}
                    """

        try:
            # Use tool-enabled LLM call
            response = self._call_llm_with_tools(prompt)

            # Parse JSON (same as before)
            json_text = response
            if '```json' in response:
                json_text = response.split('```json')[1].split('```')[0]

            judgment = json.loads(json_text.strip())
            return judgment

        except Exception as e:
            print(f"      ⚠️  Error: {e}")
            return {
                'relevant': False,
                'relevance_score': 0,
                'reasoning': f'Error: {e}',
                'key_topics': []
            }