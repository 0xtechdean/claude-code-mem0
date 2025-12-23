#!/usr/bin/env python3
"""
mem0 Stop Hook
Stores conversation context to mem0 when a session ends.

Environment Variables:
  MEM0_API_KEY: Required - Your mem0 API key from https://app.mem0.ai
  MEM0_USER_ID: Optional - User identifier for memory scoping (default: claude-code-user)
  MEM0_SAVE_MESSAGES: Optional - Number of recent messages to save (default: 10)
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
        "save_messages": int(os.environ.get("MEM0_SAVE_MESSAGES", "10")),
    }


def extract_messages(input_data: dict, max_messages: int) -> list:
    """Extract recent messages from the session transcript."""
    transcript = input_data.get("transcript", [])

    if not transcript:
        return []

    # Get the most recent messages
    recent = transcript[-max_messages:]

    messages = []
    for msg in recent:
        role = msg.get("role", "")
        content = msg.get("content", "")

        # Handle content that might be a list (multi-part messages)
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            content = " ".join(text_parts)

        if role and content and isinstance(content, str):
            # Truncate very long messages
            if len(content) > 2000:
                content = content[:2000] + "..."

            messages.append({
                "role": role,
                "content": content
            })

    return messages


def save_memories(messages: list, config: dict) -> bool:
    """Save messages to mem0."""
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=config["api_key"])
        client.add(messages, user_id=config["user_id"])
        return True
    except ImportError:
        print("mem0ai not installed. Run: pip install mem0ai", file=sys.stderr)
        return False
    except Exception as e:
        print(f"mem0 save error: {e}", file=sys.stderr)
        return False


def main():
    # Load environment from .env file
    load_env_file()

    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Get configuration
    config = get_config()

    # Check for API key
    if not config["api_key"]:
        # Silently skip if not configured
        sys.exit(0)

    # Extract messages from transcript
    messages = extract_messages(input_data, config["save_messages"])

    if not messages:
        sys.exit(0)

    # Save to mem0
    if save_memories(messages, config):
        # Output success (continue allows normal stop behavior)
        output = {"continue": True}
        print(json.dumps(output))


if __name__ == "__main__":
    main()
