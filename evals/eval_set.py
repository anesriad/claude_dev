EVALS = [
    {
        "name": "direct answer",
        "input": "Explain what an AI agent is in one sentence.",
        "must_contain": ["agent"],
        "expected_tool": None,
        "max_steps": 2
    },
    {
        "name": "calculator",
        "input": "What is 14 multiplied by 6? Use the calculator tool.",
        "must_contain": ["84"],
        "expected_tool": "calculate",
        "max_steps": 3
    },
    {
        "name": "word count",
        "input": "Count the words in: Claude builds useful tools.",
        "must_contain": ["4"],
        "expected_tool": "count_words",
        "max_steps": 3
    },
    {
        "name": "save note",
        "input": "Save this note: Client call at 3pm.",
        "must_contain": ["saved"],
        "expected_tool": "save_note",
        "max_steps": 3
    }
]
