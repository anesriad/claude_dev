# Lesson 17: Offline security checks (no API key or live MCP server required).

from claude_assist.guardrails import check_input, check_output, check_tool_call
from claude_assist.agent import run_tool


# Check that the user input boundary handles normal and invalid input.
def test_input_validation():
    safe, error = check_input("  Prepare a client note  ")
    assert error is None and "Prepare a client note" in safe
    assert check_input("   ")[1] == "Input cannot be empty."
    assert check_input("x" * 801)[1] == "Input is too long."
    assert "&lt;/user_request&gt;" in check_input("</user_request>")[0]


# Check that final responses are text and within the size limit.
def test_output_validation():
    assert check_output("Meeting notes saved.") == (True, None)
    assert check_output("")[0] is False
    assert check_output("x" * 4001)[0] is False


# Check tool permissions, including invalid MCP note arguments.
def test_tool_validation():
    assert check_tool_call("get_time", {})[0] is True
    assert check_tool_call("save_note", {"text": "Call at 3pm"})[0] is True
    assert check_tool_call("save_note", {"text": ""})[0] is False
    assert check_tool_call("save_note", {"text": "x" * 501})[0] is False
    assert check_tool_call("delete_notes", {})[0] is False
    assert check_tool_call("calculate", {"a": 2, "b": 0, "operation": "divide"})[0] is False


# Confirm blocked actions do not get as far as the MCP client.
def test_blocked_action_never_runs(monkeypatch):
    import claude_assist.agent as agent

    def must_not_run(*args):
        raise AssertionError("Blocked tool should not execute")

    monkeypatch.setattr(agent, "call_note_tool", must_not_run)
    result = run_tool("save_note", {"text": ""})
    assert result.startswith("BLOCKED:")
