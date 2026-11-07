# Lesson 18: Small application hooks for safe Claude request monitoring.
# These are Python application hooks, not Claude Code event hooks.

import time


# Record safe request metadata and the starting time; never print the prompt or key.
def before_request(model):
    print(f"[request] model={model}")
    return time.perf_counter()


# Report token usage and elapsed time after a successful Claude response.
def after_request(response, started):
    seconds = time.perf_counter() - started
    usage = response.usage
    summary = {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "seconds": seconds,
    }
    print(f"[usage] in={summary['input_tokens']} out={summary['output_tokens']}")
    print(f"[duration] {seconds:.2f}s")
    return summary


# Report a failure without logging its message, user text, or secret values.
def on_request_error(error, started):
    seconds = time.perf_counter() - started
    print(f"[request failed] type={type(error).__name__} duration={seconds:.2f}s")


# Run the request between the before/after hooks; keep errors visible to the app.
def call_with_hooks(send_request, model):
    started = before_request(model)
    try:
        response = send_request()
    except Exception as error:
        on_request_error(error, started)
        raise
    after_request(response, started)
    return response
