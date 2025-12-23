#!/usr/bin/env python3
"""
Tests for mem0 Claude Code hooks
Run with: python -m pytest tests/ -v
"""

import json
import os
import sys
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent.parent


class TestUserPromptSubmitHook:
    """Tests for userpromptsubmit.py hook"""

    def test_returns_nothing_without_api_key(self):
        """Should exit silently when no API key configured"""
        input_data = json.dumps({"prompt": "test prompt"})

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "userpromptsubmit.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0
        assert result.stdout == ""

    def test_returns_nothing_without_prompt(self):
        """Should exit silently when no prompt provided"""
        input_data = json.dumps({})

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "userpromptsubmit.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    def test_handles_invalid_json(self):
        """Should handle invalid JSON input gracefully"""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "userpromptsubmit.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    def test_accepts_user_prompt_field(self):
        """Should accept 'user_prompt' as alternative field name"""
        input_data = json.dumps({"user_prompt": "test prompt"})

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "userpromptsubmit.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    @pytest.mark.skipif(
        not os.environ.get("MEM0_API_KEY"),
        reason="MEM0_API_KEY not set"
    )
    def test_retrieves_memories_with_valid_key(self):
        """Should retrieve and output memories when API key is valid"""
        input_data = json.dumps({"prompt": "test query for memories"})

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "userpromptsubmit.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env=os.environ
        )

        assert result.returncode == 0
        # Output should be plain text with memories (if any exist)
        if result.stdout:
            assert "memories" in result.stdout.lower() or "Relevant" in result.stdout


class TestStopHook:
    """Tests for stop.py hook"""

    def test_returns_nothing_without_api_key(self):
        """Should exit silently when no API key configured"""
        input_data = json.dumps({
            "transcript": [
                {"role": "user", "content": "test message"}
            ]
        })

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "stop.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    def test_returns_nothing_without_transcript(self):
        """Should exit silently when no transcript provided"""
        input_data = json.dumps({})

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "stop.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    def test_handles_invalid_json(self):
        """Should handle invalid JSON input gracefully"""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "stop.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    def test_handles_multipart_content(self):
        """Should handle multipart content messages"""
        input_data = json.dumps({
            "transcript": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "part one"},
                        {"type": "text", "text": "part two"}
                    ]
                }
            ]
        })

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "stop.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 0

    @pytest.mark.skipif(
        not os.environ.get("MEM0_API_KEY"),
        reason="MEM0_API_KEY not set"
    )
    def test_saves_memories_with_valid_key(self):
        """Should save memories when API key is valid"""
        input_data = json.dumps({
            "transcript": [
                {"role": "user", "content": "Test save from pytest Claude Code"}
            ]
        })

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "stop.py")],
            input=input_data,
            capture_output=True,
            text=True,
            env=os.environ
        )

        assert result.returncode == 0
        if result.stdout:
            output = json.loads(result.stdout)
            assert output.get("continue") == True


class TestManualSaveScript:
    """Tests for save_manual.py script"""

    def test_returns_error_without_api_key(self):
        """Should return error when no API key configured"""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "save_manual.py"), "test message"],
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        assert result.returncode == 1
        output = json.loads(result.stdout)
        assert output["success"] == False

    def test_accepts_command_line_argument(self):
        """Should accept message as command line argument"""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "save_manual.py"), "test", "message"],
            capture_output=True,
            text=True,
            env={**os.environ, "MEM0_API_KEY": "", "CLAUDE_PROJECT_DIR": ""}
        )

        # Should fail due to missing API key, not argument parsing
        output = json.loads(result.stdout)
        assert "error" in output

    @pytest.mark.skipif(
        not os.environ.get("MEM0_API_KEY"),
        reason="MEM0_API_KEY not set"
    )
    def test_saves_with_valid_key(self):
        """Should save successfully with valid API key"""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "save_manual.py"), "Test from pytest manual save"],
            capture_output=True,
            text=True,
            env=os.environ
        )

        output = json.loads(result.stdout)
        assert output["success"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
