# test_llm.py
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

model = os.getenv("LITELLM_MODEL")  # e.g. claude-haiku-4-5-20251001

response = completion(
    model=model,
    messages=[{"role": "user", "content": "Say hello!"}],
)

print(response.choices[0].message.content)
print("✅ LiteLLM working!")