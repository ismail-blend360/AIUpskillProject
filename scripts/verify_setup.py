#!/usr/bin/env python3
"""
Verify the local dev environment is ready for Milestone 1.

Run from the repo root:

    python scripts/verify_setup.py

Checks Python version, dependencies, .env, and that LiteLLM can reach the
configured model. Prints a green ✅ for each step or a red ✗ with the fix.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


REQUIRED_PYTHON = (3, 11)
REQUIRED_PACKAGES = [
    "aiohttp",
    "feedparser",
    "litellm",
    "mcp",
    "dotenv",  # python-dotenv exposes itself as `dotenv`
    "pytest",
]
PROVIDER_KEYS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY")


def fail(msg: str, fix: str = "") -> None:
    print(f"✗ {msg}")
    if fix:
        print(f"  → {fix}")
    sys.exit(1)


def check_python_version() -> None:
    if sys.version_info < REQUIRED_PYTHON:
        fail(
            f"Python version: {sys.version.split()[0]} (need ≥ 3.11)",
            "Install Python 3.11+ from python.org, then recreate venv.",
        )
    print(f"✅ Python version: {sys.version.split()[0]}")


def check_venv() -> None:
    # sys.prefix differs from sys.base_prefix when inside a venv.
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        fail(
            "Virtual environment: not active",
            "Run `source venv/bin/activate` (macOS/Linux) "
            "or `venv\\Scripts\\activate` (Windows).",
        )
    print("✅ Virtual environment: Active")


def check_dependencies() -> None:
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        fail(
            f"Dependencies: missing {', '.join(missing)}",
            "Run `pip install -r requirements.txt`.",
        )
    print("✅ Dependencies: All installed")


def check_env() -> tuple[str, str]:
    from dotenv import load_dotenv

    env_path = Path(".env")
    if not env_path.exists():
        fail(
            ".env file: not found",
            "Run `cp .env.example .env` and paste your provider key.",
        )
    load_dotenv(env_path)

    model = os.getenv("LITELLM_MODEL")
    if not model:
        fail(
            "LITELLM_MODEL: not set in .env",
            "Add `LITELLM_MODEL=claude-haiku-4-5-20251001` "
            "(or any LiteLLM-supported model string) to .env.",
        )

    provider_key = next(
        (k for k in PROVIDER_KEYS if os.getenv(k)),
        None,
    )
    if not provider_key:
        fail(
            "API keys: no provider key set",
            f"Uncomment and fill one of {', '.join(PROVIDER_KEYS)} in .env.",
        )
    print("✅ API keys: Configured")
    return model, provider_key


def check_project_structure() -> None:
    required = ["src", "tests", "docs", "data", "requirements.txt", ".env.example"]
    missing = [p for p in required if not Path(p).exists()]
    if missing:
        fail(
            f"Project structure: missing {', '.join(missing)}",
            "Did you clone the repo and `cd AIUpskillProject`?",
        )
    print("✅ Project structure: Valid")


def check_imports() -> None:
    try:
        import src  # noqa: F401
    except Exception as exc:
        fail(
            f"Import paths: cannot import `src` ({exc})",
            "Make sure you ran `pip install -r requirements.txt` and that "
            "the venv is active.",
        )
    print("✅ Import paths: Working")


def check_litellm_completion(model: str) -> None:
    """Confirm we can actually reach the configured model."""
    try:
        from litellm import completion

        resp = completion(
            model=model,
            messages=[{"role": "user", "content": "Reply with just: OK"}],
            max_tokens=5000 ,
        )
        # LiteLLM normalizes to OpenAI-style responses
        text = resp["choices"][0]["message"]["content"].strip()
        if not text:
            fail(
                f"LiteLLM call to {model}: empty response",
                "Check provider status; try a different LITELLM_MODEL.",
            )
    except Exception as exc:
        fail(
            f"LiteLLM call to {model}: {exc}",
            "Verify the model string matches your provider key, and that the "
            "key has access. See https://docs.litellm.ai/docs/providers",
        )
    print(f"✅ LiteLLM ({model}): Working")


def main() -> None:
    print("🔍 Verifying AI Upskill Project setup...\n")
    check_python_version()
    check_venv()
    check_dependencies()
    model, _ = check_env()
    check_project_structure()
    check_imports()
    check_litellm_completion(model)
    print(
        "\n🎉 Setup complete! Ready to start Milestone 1.\n\n"
        "Next steps:\n"
        "1. Read docs/architecture/overview.md\n"
        "2. Start Milestone 1 tomorrow\n"
        "3. Join Slack: #ai-upskill-cohort-[X]\n"
    )


if __name__ == "__main__":
    main()
