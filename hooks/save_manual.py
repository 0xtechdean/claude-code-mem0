#!/usr/bin/env python3
"""
mem0 Manual Save Script
Saves provided messages to mem0 memory.

Usage: echo '{"messages": [...]}' | python3 save_manual.py
Or: python3 save_manual.py "message to save"
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
    }


def save_memories(messages: list, config: dict) -> dict:
    """Save messages to mem0."""
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=config["api_key"])
        result = client.add(messages, user_id=config["user_id"])
        return {"success": True, "result": result}
    except ImportError:
        return {"success": False, "error": "mem0ai not installed. Run: pip install mem0ai"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    # Load environment from .env file
    load_env_file()

    # Get configuration
    config = get_config()

    # Check for API key
    if not config["api_key"]:
        print(json.dumps({"success": False, "error": "MEM0_API_KEY not configured"}))
        sys.exit(1)

    # Get messages from stdin or command line
    messages = []

    if len(sys.argv) > 1:
        # Message provided as command line argument
        content = " ".join(sys.argv[1:])
        messages = [{"role": "user", "content": content}]
    else:
        # Try to read from stdin
        try:
            input_data = json.load(sys.stdin)
            if isinstance(input_data, dict) and "messages" in input_data:
                messages = input_data["messages"]
            elif isinstance(input_data, list):
                messages = input_data
        except:
            print(json.dumps({"success": False, "error": "No messages provided"}))
            sys.exit(1)

    if not messages:
        print(json.dumps({"success": False, "error": "No messages to save"}))
        sys.exit(1)

    # Save to mem0
    result = save_memories(messages, config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
