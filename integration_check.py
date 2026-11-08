# Lesson 19: Offline integration checks for the existing Claude Assist app.
# Fake Claude responses and an in-memory note save avoid live API and MCP calls.

from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from claude_assist import agent, config
from claude_assist.guardrails import check_input, check_tool_call
from claude_assist.hooks import call_with_hooks
from claude_assist.tools import dispatch


# Build one fake Claude tool-use response for an integration test.
def tool_response(name, arguments, request_id):
    block = SimpleNamespace(type="tool_use", name=name, input=arguments, id=request_id)
    return SimpleNamespace(stop_reason="tool_use", content=[block])


# Build a final text response, like an end_turn from Claude.
def final_response(text):
    
    block = SimpleNamespace(type="text", text=text)
    return SimpleNamespace(stop_reason="end_turn", content=[block])

# Run the existing agent against scripted responses, not the real API.
def check_agent_flow():
    note = "Client call prep: review goals, risks, next steps, and key questions."
    responses = iter([
        tool_response("get_time", {}, "tool-1"),
        tool_response("count_words", {"text": note}, "tool-2"),
        tool_response("save_note", {"text": note}, "tool-3"),
        final_response("The client-call note was saved."),
    ])
    sent_messages = []
    saved_notes = []

    # Keep a copy of each messages list to inspect the request/result pairs.
    def fake_create(**kwargs):
        sent_messages.append(list(kwargs["messages"]))
        return next(responses)

    fake_client = SimpleNamespace(messages=SimpleNamespace(create=fake_create))

    def fake_save(name, args):
        assert name == "save_note"
        saved_notes.append(args["text"])
        return "Note saved."

    # Use the existing agent code, replacing only external connections.
    with patch.object(agent.anthropic, "Anthropic", return_value=fake_client), \
         patch.object(agent, "call_note_tool", side_effect=fake_save), \
         redirect_stdout(StringIO()):
        result = agent.run_agent("Prepare and save a short client-call note.", return_trace=True)

    assert result["tools_used"] == ["get_time", "count_words", "save_note"]
    assert result["steps"] == 4
    assert "saved" in result["answer"].lower()
    assert saved_notes == [note]
    # Check that Claude sees tool_result messages after requesting each tool.
    for tool_id in ("tool-1", "tool-2", "tool-3"):
        assert any(
            any(block.get("tool_use_id") == tool_id for block in msg["content"])
            for history in sent_messages for msg in history
            if msg["role"] == "user" and isinstance(msg["content"], list)
        )
    return result


# Prove invalid input and a blocked MCP action cannot perform work.
def check_security():
    assert check_input("   ")[1] == "Input cannot be empty."
    assert check_tool_call("save_note", {"text": ""})[0] is False
    with patch.object(agent, "call_note_tool", side_effect=AssertionError("MCP ran")):
        assert agent.run_tool("save_note", {"text": ""}).startswith("BLOCKED:")
    return True


# Verify the local dispatcher and safe request hooks still work together.
def check_tools_and_hooks():
    assert dispatch("calculate", {"a": 14, "b": 6, "operation": "multiply"}) == 84
    assert dispatch("count_words", {"text": "Claude builds useful tools"}) == 4
    fake = SimpleNamespace(usage=SimpleNamespace(input_tokens=23, output_tokens=7))
    output = StringIO()
    with redirect_stdout(output):
        assert call_with_hooks(lambda: fake, "test-model") is fake
    assert "in=23 out=7" in output.getvalue()
    assert "[duration]" in output.getvalue()
    return True


# Ensure missing keys fail clearly without using any actual credentials.
def check_configuration():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "fake-test-key"}):
        assert config.require_api_key() == "fake-test-key"
    with patch.dict("os.environ", {}, clear=True):
        try:
            config.require_api_key()
        except RuntimeError as error:
            assert "Missing ANTHROPIC_API_KEY" in str(error)
        else:
            raise AssertionError("Missing API key was not rejected")
    return True


# Run all offline checks and print a short report for Lesson 19.
def main():
    checks = [
        ("Config and missing key", check_configuration),
        ("Local tools and hooks", check_tools_and_hooks),
        ("Guardrails block unsafe actions", check_security),
        ("Agent + local tools + MCP result", check_agent_flow),
    ]
    for title, function in checks:
        function()
        print(f"PASS | {title}")
    print(f"\n{len(checks)}/{len(checks)} offline integration checks passed.")
    print("Live capstone run comes in Lesson 20.")


if __name__ == "__main__":
    main()
