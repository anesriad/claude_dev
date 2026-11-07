# Lesson 18: Read Claude settings and secrets without storing keys in code.
# Update the existing claude_assist/config.py; keep any custom model settings you already use.

import os
from dotenv import load_dotenv

# Local development only: load .env when it exists. Deployed apps can use environment variables.
load_dotenv()

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = 1024
SYSTEM = "You are Claude Assist. Be helpful, clear, and use tools when useful."


# Check a required key at application startup, without printing its value.
def require_api_key():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key or not key.strip():
        raise RuntimeError("Missing ANTHROPIC_API_KEY. Set it in your environment.")
    return key
