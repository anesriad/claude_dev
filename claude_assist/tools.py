from datetime import datetime


# Perform basic arithmetic after checking the inputs.
def calculate(a, b, operation):
    if not isinstance(a, (int, float)):
        return "error: a must be a number"

    if not isinstance(b, (int, float)):
        return "error: b must be a number"

    if operation not in ["add", "subtract", "multiply", "divide"]:
        return "error: invalid operation"

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if b == 0:
        return "error: cannot divide by zero"

    return a / b


# Return the current local time.
def get_time():
    return datetime.now().strftime("%H:%M") 


# Count the words in some text.
def count_words(text):
    if not isinstance(text, str):
        return "error: text must be a string"

    if len(text) > 1000:
        return "error: text is too long"

    return len(text.split())


# Describe the calculator tool for Claude.
CALCULATOR_TOOL = {
    "name": "calculate",
    "description": "Use this tool for exact basic arithmetic with two numbers.",
    "input_schema": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"},
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"]
            }
        },
        "required": ["a", "b", "operation"]
    }
}


# Describe the time tool for Claude.
TIME_TOOL = {
    "name": "get_time",
    "description": "Use this tool when the user asks for the current local time.",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}


# Describe the word-count tool for Claude.
WORD_COUNT_TOOL = {
    "name": "count_words",
    "description": "Use this tool to count the words in a piece of text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        },
        "required": ["text"]
    }
}


# Register all tool definitions together for the API call.
TOOL_DEFINITIONS = [
    CALCULATOR_TOOL,
    TIME_TOOL,
    WORD_COUNT_TOOL
]


# Map tool names to the Python functions that run them.
TOOLS = {
    "calculate": calculate,
    "get_time": get_time,
    "count_words": count_words
}


# Run the function that matches the requested tool name.
def dispatch(name, args):
    fn = TOOLS.get(name)

    if fn is None:
        return f"error: unknown tool '{name}'"

    return fn(**args) #calls the function it found
