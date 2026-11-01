'''
mcp_notes.py is a small adapter. 
It lets the rest of your assistant code call the tools in your notes 
MCP server (mcp_server.py) as if they were ordinary Python functions.
'''

import asyncio

from mcp import Client
from mcp_server import mcp


# Call the notes MCP server from async code.
async def call_note_tool_async(name, args):
    # Connects to the notes server and calls a tool.
    async with Client(mcp) as client:
        result = await client.call_tool(name, args)

    # Return the first text result in a simple form.
    if result.content:
        block = result.content[0]

        if hasattr(block, "text"):
            return block.text

    return str(result.structured_content)


# Call the notes MCP server from normal Python code.
def call_note_tool(name, args):
    #starts the async machinery, runs the function to completion, and hands back the result.
    return asyncio.run(
        call_note_tool_async(name, args)
    )
