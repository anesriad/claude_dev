import anthropic
from dotenv import load_dotenv

from claude_assist import config
from claude_assist.tools import TOOL_DEFINITIONS, TOOLS as LOCAL_TOOLS, dispatch
from claude_assist.mcp_notes import call_note_tool


load_dotenv()

MAX_STEPS = 6


# Describe the MCP note tool so Claude can choose it.
MCP_NOTE_TOOL = {
    "name": "save_note",
    "description": "Save a short note for later.",
    "input_schema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        },
        "required": ["text"]
    }
}


# Claude sees one toolbox containing local and MCP tools.
TOOLS = TOOL_DEFINITIONS + [MCP_NOTE_TOOL]


# Run the requested tool in the correct place.
def run_tool(name, args):
    if name in LOCAL_TOOLS:
        return dispatch(name, args)

    if name == "save_note":
        return call_note_tool(name, args)

    return f"Unknown tool: {name}"


# Run a bounded plan-act-observe agent loop.
def run_agent(goal):
    client = anthropic.Anthropic()

    messages = [
        {
            "role": "user",
            "content": goal
        }
    ]

    for step in range(MAX_STEPS):
        resp = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            system=config.SYSTEM,
            tools=TOOLS,
            messages=messages
        )

        # Keep Claude's response in the history.
        messages.append({
            "role": "assistant",
            "content": resp.content
        })

        # Natural stop: Claude gives a final answer.
        if resp.stop_reason != "tool_use":
            for block in resp.content:
                if block.type == "text":
                    return block.text

            return "Claude finished without a text response."

        results = []

        # Run every tool Claude requested in this step.
        for block in resp.content:
            if block.type == "tool_use":
                print(f"[step {step + 1}] tool:", block.name)
                print("input:", block.input)

                result = run_tool(
                    block.name,
                    block.input
                )

                print(f"[step {step + 1}] result:", result)

                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        # Feed all tool results back to Claude.
        messages.append({
            "role": "user",
            "content": results
        })

    return "Stopped after reaching the step limit."


# Run one concrete agent task when this file is executed directly.
if __name__ == "__main__":
    goal = (
        "Prepare a concise client-call prep note. "
        "Check the current local time. "
        "Keep the final note under 25 words. "
        "Use the word-count tool to verify the length. "
        "If it is too long, revise it and check again. "
        "Then save the final note."
    )

    print(run_agent(goal))
