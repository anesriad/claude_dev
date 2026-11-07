# Lesson 18: Offline tests for safe secret loading and request hooks.
# No real API key or Claude request is used in these tests.

from types import SimpleNamespace
import pytest

from claude_assist import config
from claude_assist.hooks import call_with_hooks, after_request


# A missing API key should fail clearly without exposing a credential.
def test_missing_key_fails(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="Missing ANTHROPIC_API_KEY"):
        config.require_api_key()


# A present fake key should be read from the environment.
def test_key_reads_environment(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-tests")
    assert config.require_api_key() == "fake-key-for-tests"


# Hooks should keep the response and print token counts without the private prompt.
def test_hooks_measure_response_without_logging_text(capsys):
    fake = SimpleNamespace(usage=SimpleNamespace(input_tokens=23, output_tokens=7))
    response = call_with_hooks(lambda: fake, "test-model")
    log = capsys.readouterr().out
    assert response is fake
    assert "in=23 out=7" in log
    assert "[duration]" in log
    assert "private meeting details" not in log


# A failed request should report its error type, but not its error message.
def test_failure_does_not_log_secret(capsys):
    def fail():
        raise ValueError("SECRET-DO-NOT-LOG")

    with pytest.raises(ValueError):
        call_with_hooks(fail, "test-model")
    log = capsys.readouterr().out
    assert "type=ValueError" in log
    assert "SECRET-DO-NOT-LOG" not in log


# The after hook should return measurements that could be stored or tested.
def test_after_hook_returns_summary():
    from time import perf_counter
    fake = SimpleNamespace(usage=SimpleNamespace(input_tokens=5, output_tokens=2))
    summary = after_request(fake, perf_counter())
    assert summary["input_tokens"] == 5
    assert summary["output_tokens"] == 2
    assert summary["seconds"] >= 0
