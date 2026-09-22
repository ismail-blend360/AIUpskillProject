# llm_examples.py
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
model = os.getenv("LITELLM_MODEL")


def ask(prompt: str) -> str:
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# Example 1: Simple completion
print("Example 1:", ask("Explain async/await in Python in one sentence"))

# Example 2: JSON output
print("\nExample 2:", ask("""
Given this article title: "New AI Model Released"
Output JSON with these fields: relevant (boolean), reason (string)

{"relevant": true/false, "reason": "explanation"}
"""))

# Example 3: Few-shot learning
print("\nExample 3:", ask("""
Classify articles as AI-related or not.

Examples:
Title: "GPT-4 Released" -> AI-related: Yes
Title: "Recipe for Pasta" -> AI-related: No
Title: "Machine Learning in Healthcare" -> AI-related: Yes

Now classify:
Title: "New JavaScript Framework"
"""))