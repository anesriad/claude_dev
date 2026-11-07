# Claude Assist

## Project purpose
Claude Assist is a learning project built with Python and the Anthropic API. It includes local tools, an MCP notes server, and a small agent loop.

## Key files
- `claude_assist/agent.py` - bounded agent loop
- `claude_assist/tools.py` - local tools and dispatcher
- `claude_assist/mcp_notes.py` - helper for the MCP notes tool
- `mcp_server.py` - notes MCP server

## Useful commands
```bash
python -m claude_assist.agent
pytest
```

## Working rules
- Explain the relevant code before editing it.
- Keep changes small and focused.
- Do not change unrelated files.
- Run the relevant tests after a change.
- Show the diff before the change is kept.
