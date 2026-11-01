from mcp.server import MCPServer


# Create a small MCP server for notes.
mcp = MCPServer("notes")

# Keep notes in memory for this lesson.
NOTES = []


# Save one note.
@mcp.tool()
def save_note(text: str) -> str:
    """Save a note."""
    NOTES.append(text)
    return "Note saved."


# Return all saved notes.
@mcp.tool()
def get_notes() -> list[str]:
    """Return all saved notes."""
    return NOTES


# Start the MCP server when this file is run directly.
if __name__ == "__main__":
    mcp.run()