"""Simple calculator tool."""

from typing import Any, Dict


def calculator(expression: str) -> Dict[str, Any]:
    """
    Evaluate mathematical expression.

    Args:
        expression: Math expression (e.g., "2 + 2", "10 * 5")

    Returns:
        Dict with result or error
    """
    try:
        # Safe eval with limited scope
        result = eval(expression, {"__builtins__": {}}, {})
        return {"success": True, "result": result, "expression": expression}
    except Exception as e:
        return {"success": False, "error": str(e), "expression": expression}


# Tool schema for LLM — OpenAI / LiteLLM format
CALCULATOR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Evaluate mathematical expressions. Use for arithmetic calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')",
                }
            },
            "required": ["expression"],
        },
    },
}


# Test
if __name__ == "__main__":
    print(calculator("2 + 2"))
    print(calculator("10 * 5 + 3"))
    print(calculator("invalid"))
