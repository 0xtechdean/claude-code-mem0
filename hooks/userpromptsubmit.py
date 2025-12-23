#!/usr/bin/env python3
"""
mem0 UserPromptSubmit Hook
Searches mem0 for relevant memories before each prompt and injects them into context.

Environment Variables:
  MEM0_API_KEY: Required - Your mem0 API key from https://app.mem0.ai
  MEM0_USER_ID: Optional - User identifier for memory scoping (default: claude-code-user)
  MEM0_TOP_K: Optional - Number of memories to retrieve (default: 5)
  MEM0_THRESHOLD: Optional - Minimum similarity score (default: 0.3)
"""

import json
import os
import sys
from pathlib import Path


def load_env_file():
    """Load .env file from project directory if it exists."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        env_path = Path(project_dir) / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())


def get_config():
    """Get configuration from environment variables."""
    return {
        "api_key": os.environ.get("MEM0_API_KEY", ""),
        "user_id": os.environ.get("MEM0_USER_ID", "claude-code-user"),
        "top_k": int(os.environ.get("MEM0_TOP_K", "5")),
        "threshold": float(os.environ.get("MEM0_THRESHOLD", "0.3")),
    }


def search_memories(query: str, config: dict) -> list:
    """Search mem0 for relevant memories."""
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=config["api_key"])
        response = client.search(
            query=query,
            filters={"user_id": config["user_id"]},
            top_k=config["top_k"],
            threshold=config["threshold"]
        )
        # Handle both dict response {"results": [...]} and list response
        if isinstance(response, dict):
            return response.get("results", [])
        return response if isinstance(response, list) else []
    except ImportError:
        print("mem0ai not installed. Run: pip install mem0ai", file=sys.stderr)
        return []
    except Exception as e:
        print(f"mem0 search error: {e}", file=sys.stderr)
        return []


def format_memories(results: list) -> str:
    """Format memories for context injection."""
    memories = []
    for r in results:
        memory = r.get("memory", "")
        if memory:
            # Include category if available
            categories = r.get("categories", [])
            if categories:
                memories.append(f"- [{', '.join(categories)}] {memory}")
            else:
                memories.append(f"- {memory}")

    if not memories:
        return ""

    return "## Relevant memories from previous conversations:\n" + "\n".join(memories)


def main():
    # Load environment from .env file
    load_env_file()

    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Get user prompt
    user_prompt = input_data.get("user_prompt", "")
    if not user_prompt:
        sys.exit(0)

    # Get configuration
    config = get_config()

    # Check for API key
    if not config["api_key"]:
        # Silently skip if not configured
        sys.exit(0)

    # Search for relevant memories
    results = search_memories(user_prompt, config)

    # Format and output memories
    if results:
        message = format_memories(results)
        if message:
            output = {
                "continue": True,
                "message": message
            }
            print(json.dumps(output))


if __name__ == "__main__":
    main()
