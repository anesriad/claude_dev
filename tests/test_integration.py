# Lesson 19: Repeatable integration tests for the existing Claude Assist code.
# These checks use fake API and MCP results; no live services or keys are needed.

from integration_check import (
    check_agent_flow,
    check_configuration,
    check_security,
    check_tools_and_hooks,
)


# An absent key must stop the app clearly; a fake key should be accepted.
def test_configuration_boundary():
    assert check_configuration() is True


# Validate that local tools and token-usage hooks still work together.
def test_local_tools_and_hooks():
    assert check_tools_and_hooks() is True


# A blocked note request must never reach the MCP server.
def test_blocked_action_does_not_execute():
    assert check_security() is True


# Claude tool requests, result history, and the final answer work as one flow.
def test_meeting_prep_agent_flow():
    result = check_agent_flow()
    assert result["tools_used"] == ["get_time", "count_words", "save_note"]
    assert result["blocked_tools"] == []
    assert "saved" in result["answer"].lower()
