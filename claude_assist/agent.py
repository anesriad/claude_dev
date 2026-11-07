# Lesson 17: Same Claude agent as before, now with guardrails at key boundaries.
# Keep this file as claude_assist/agent.py in the student project.

import anthropic
from dotenv import load_dotenv

from claude_assist import config
from claude_assist.tools import TOOL_DEFINITIONS, TOOLS as LOCAL_TOOLS, dispatch
from claude_assist.mcp_notes import call_note_tool
from claude_assist.guardrails import check_input, check_output, check_tool_call

load_dotenv()
MAX_STEPS = 6

MCP_NOTE_TOOL = {
    "name": "save_note",
    "description": "Save a short note for later.",
    "input_schema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"]
    }
}
TOOLS = TOOL_DEFINITIONS + [MCP_NOTE_TOOL]


# Check a requested action before routing it to a local or MCP tool.
def run_tool(name, args):
    allowed, reason = check_tool_call(name, args)
    if not allowed:
        return f"BLOCKED: {reason}"

    if name in LOCAL_TOOLS:
        return str(dispatch(name, args))
    if name == "save_note":
        return str(call_note_tool(name, args))
    return "BLOCKED: Tool not allowed."


# Find the first text block in Claude's response.
def read_text(resp):
    for block in resp.content:
        if block.type == "text":
            return block.text
    return ""


# Return a normal answer, or a small trace for Lesson 16 evaluations.
def finish(answer, tools_used, steps, blocked_tools, return_trace):
    if return_trace:
        return {
            "answer": answer,
            "tools_used": tools_used,
            "steps": steps,
            "blocked_tools": blocked_tools,
        }
    return answer


# Run Claude's bounded tool loop with checks at input, tool, and output.
def run_agent(goal, return_trace=False):
    safe_goal, reason = check_input(goal)
    if reason:
        return finish(f"Input rejected: {reason}", [], 0, [], return_trace)

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": safe_goal}]
    tools_used = []
    blocked_tools = []

    for step in range(MAX_STEPS):
        resp = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            system=config.SYSTEM,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": resp.content})

        # Only return a complete final answer after validating it.
        if resp.stop_reason != "tool_use":
            if resp.stop_reason != "end_turn":
                answer = f"Stopped: unexpected response ({resp.stop_reason})."
            else:
                answer = read_text(resp)
                valid, error = check_output(answer)
                if not valid:
                    answer = f"Response blocked: {error}"
            return finish(answer, tools_used, step + 1, blocked_tools, return_trace)

        results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue

            allowed, error = check_tool_call(block.name, block.input)
            if not allowed:
                blocked_tools.append(block.name)
                result = f"BLOCKED: {error}"
            else:
                # A valid request is run by our app, not by the model itself.
                tools_used.append(block.name)
                result = run_tool(block.name, block.input)

            # Log only the tool name and status, not private text or secrets.
            print(f"[step {step + 1}] {block.name}: "
                  f"{'allowed' if allowed else 'blocked'}")
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
                "is_error": not allowed
            })

        # Keep tool_result linked to the matching tool_use in history.
        messages.append({"role": "user", "content": results})

    return finish("Stopped after reaching the step limit.", tools_used,
                  MAX_STEPS, blocked_tools, return_trace)
