from claude_assist.tools import calculate, count_words, dispatch


def test_dispatch_unknown():
    result = dispatch("does_not_exist", {})
    assert "unknown" in result.lower()


def test_division_by_zero():
    result = calculate(10, 0, "divide")
    assert "cannot divide by zero" in result.lower()


def test_count_words():
    result = count_words("Claude builds useful tools")
    assert result == 4
