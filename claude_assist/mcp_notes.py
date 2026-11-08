# Lesson 20: Reuse the Lesson 14 MCP client for both save_note and get_notes.
# The MCP server runs in-process for this small local teaching application.

import asyncio
from mcp import Client
from mcp_server import mcp

# Call a notes tool through the MCP client from asynchronous code.
async def call_note_tool_async(name, args):
    async with Client(mcp) as client:
        result = await client.call_tool(name, args)

    if result.is_error:
        raise RuntimeError("The MCP notes tool returned an error.")

    # Prefer a plain text result when the server supplies one.
    if result.content:
        block = result.content[0]
        if hasattr(block, "text"):
            return block.text
    return str(result.structured_content)

# Let the normal synchronous Python agent call the asynchronous MCP client.
def call_note_tool(name, args):
    return asyncio.run(call_note_tool_async(name, args))
