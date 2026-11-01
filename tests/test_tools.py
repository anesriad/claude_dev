from claude_assist.tools import calculate


def test_addition():
    assert calculate(2, 3, "add") == 5


def test_division():
    assert calculate(10, 4, "divide") == 2.5


def test_division_by_zero():
    assert calculate(10, 0, "divide") == "error: cannot divide by zero"


def test_invalid_operation():
    assert calculate(2, 3, "power") == "error: invalid operation"
