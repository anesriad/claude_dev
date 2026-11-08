# Lesson 20: Same MCP notes server, now saving notes in a local JSON file.
# The file is local demo data; do not commit notes containing private information.

import json
import os
from pathlib import Path
from mcp.server import MCPServer

mcp = MCPServer("notes")

# Choose the local file used to keep notes between application runs.
def notes_path():
    return Path(os.getenv("CLAUDE_NOTES_FILE", "notes.json"))

# Read saved notes; start with an empty list when the file does not exist.
def load_notes():
    path = notes_path()
    if not path.exists():
        return []
    notes = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(notes, list) or not all(isinstance(x, str) for x in notes):
        raise ValueError("The notes file must contain a list of text notes.")
    return notes

# Save the full note to disk so it is available after restarting the app.
@mcp.tool()
def save_note(text: str) -> str:
    """Save a meeting or project brief for later."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Note text cannot be empty.")
    if len(text) > 2500:
        raise ValueError("Note is too long.")
    notes = load_notes()
    notes.append(text)
    path = notes_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")
    return "Note saved."

# Return the latest 10 stored notes for the assistant to review.
@mcp.tool()
def get_notes() -> list[str]:
    """Read the latest saved notes."""
    return load_notes()[-10:]

# Start this MCP server directly when running it as a script.
if __name__ == "__main__":
    mcp.run()
