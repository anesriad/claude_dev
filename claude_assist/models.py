"""Simple model helpers for Lesson 7."""

HAIKU_MODEL = "claude-haiku-5-5"
SONNET_MODEL = "claude-sonnet-5-5"
OPUS_MODEL = "claude-opus-5-5"
FABLE_MODEL = "claude-fable-5-1"

# Available reasoning effort levels.
EFFORT_LEVELS = ["low", "medium", "high", "xhigh", "max"]

def pick_model(task):
    if task == "simple":
        return HAIKU_MODEL

    if task == "hard":
        return OPUS_MODEL

    if task == "frontier":
        return FABLE_MODEL

    return SONNET_MODEL

def read_usage(resp):
    return (
        resp.usage.input_tokens,
        resp.usage.output_tokens
    )