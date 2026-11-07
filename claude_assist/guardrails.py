# Lesson 17: Small input, output, and tool checks for Claude Assist.
# These are extra safety checks, not a complete prompt-injection defence.

from html import escape
import math

MAX_INPUT_LENGTH = 800
MAX_OUTPUT_LENGTH = 4000
MAX_NOTE_LENGTH = 500


# Validate input and label it as untrusted user text.
def check_input(text):
    if not isinstance(text, str):
        return None, "Input must be text."

    text = text.strip()
    if not text:
        return None, "Input cannot be empty."
    if len(text) > MAX_INPUT_LENGTH:
        return None, "Input is too long."

    # Escaping prevents user text from closing our example XML tags.
    # The tags are a signal to Claude, not a security boundary by themselves.
    return f"<user_request>{escape(text)}</user_request>", None


# Validate a final text answer before returning it to the user.
def check_output(reply):
    if not isinstance(reply, str) or not reply.strip():
        return False, "Empty or invalid response."
    if len(reply) > MAX_OUTPUT_LENGTH:
        return False, "Response is too long."
    return True, None


# Check the name and arguments before ANY requested tool is executed.
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
            return False, "Note is too long."
        return True, None

    if name == "get_time":
        return (True, None) if not args else (False, "get_time takes no inputs.")

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
