# Lesson 20: The Lesson 17 checks, with a longer meeting brief and a read-only notes tool.
# Tags help identify user content; they do not make prompt injection impossible.

from html import escape
import math

MAX_INPUT_LENGTH = 1200
MAX_OUTPUT_LENGTH = 5000
MAX_NOTE_LENGTH = 2500

# Check user text before sending it to Claude.
def check_input(text):
    if not isinstance(text, str):
        return None, "Input must be text."
    text = text.strip()
    if not text:
        return None, "Input cannot be empty."
    if len(text) > MAX_INPUT_LENGTH:
        return None, f"Input is too long (max {MAX_INPUT_LENGTH} characters)."
    return f"<user_request>{escape(text)}</user_request>", None

# Check the final answer is valid text of a reasonable size.
def check_output(reply):
    if not isinstance(reply, str) or not reply.strip():
        return False, "Empty or invalid response."
    if len(reply) > MAX_OUTPUT_LENGTH:
        return False, "Response is too long."
    return True, None

# Validate tool names and inputs before running any Python or MCP tool.
def check_tool_call(name, args):
    if not isinstance(args, dict):
        return False, "Tool arguments must be an object."

    if name == "save_note":
        if set(args) != {"text"}:
            return False, "save_note accepts only text."
        text = args["text"]
        if not isinstance(text, str) or not text.strip():
            return False, "Note text is required."
        if len(text) > MAX_NOTE_LENGTH:
            return False, f"Note is too long (max {MAX_NOTE_LENGTH} characters)."
        return True, None

    # A read-only tool needs no inputs.
    if name in ("get_notes", "get_time"):
        return (True, None) if not args else (False, f"{name} takes no inputs.")

    if name == "count_words":
        if set(args) != {"text"} or not isinstance(args.get("text"), str):
            return False, "count_words needs text."
        if len(args["text"]) > 1000:
            return False, "Text is too long for count_words."
        return True, None

    if name == "calculate":
        if set(args) != {"a", "b", "operation"}:
            return False, "calculate needs a, b, and operation."
        for key in ("a", "b"):
            value = args[key]
            if type(value) not in (int, float) or not math.isfinite(value):
                return False, f"{key} must be a finite number."
        if args["operation"] not in ("add", "subtract", "multiply", "divide"):
            return False, "Invalid calculation operation."
        if args["operation"] == "divide" and args["b"] == 0:
            return False, "Cannot divide by zero."
        return True, None

    return False, f"Tool not allowed: {name}"
