# Lesson 18: The existing Conversation class now measures Claude API requests.
# It keeps the Lesson 17 guardrails and uses safe application hooks.

import anthropic
from claude_assist import config
from claude_assist.hooks import call_with_hooks
from claude_assist.tools import TOOL_DEFINITIONS, dispatch
from claude_assist.guardrails import check_input, check_output, check_tool_call

MAX_STEPS = 6


class Conversation:
    # Validate the API key when starting the app, then create the client and history.
    def __init__(self, system):
        key = config.require_api_key()
        self.client = anthropic.Anthropic(api_key=key)
        self.system = system
        self.history = []

    # Send one user turn, using request hooks and the existing security checks.
    def send(self, text):
        safe_text, error = check_input(text)
        if error:
            return f"Input rejected: {error}"
        self.history.append({"role": "user", "content": safe_text})

        for step in range(MAX_STEPS):
            # The hooks surround the API call, not the entire conversation loop.
            resp = call_with_hooks(
                lambda: self.client.messages.create(
                    model=config.MODEL,
                    max_tokens=config.MAX_TOKENS,
                    system=self.system,
                    tools=TOOL_DEFINITIONS,
                    messages=self.history,
                ),
                config.MODEL,
            )
            self.history.append({"role": "assistant", "content": resp.content})

            # Accept only a completed and validated final response.
            if resp.stop_reason != "tool_use":
                if resp.stop_reason != "end_turn":
                    return f"Stopped: unexpected response ({resp.stop_reason})."
                reply = next((b.text for b in resp.content if b.type == "text"), "")
                valid, reason = check_output(reply)
                return reply if valid else f"Response blocked: {reason}"

            results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue

                # Validate each tool request before it runs.
                allowed, reason = check_tool_call(block.name, block.input)
                if allowed:
                    try:
                        result = str(dispatch(block.name, block.input))
                    except (TypeError, ValueError) as error:
                        allowed = False
                        result = f"BLOCKED: Invalid tool arguments ({type(error).__name__})."
                else:
                    result = f"BLOCKED: {reason}"

                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                    "is_error": not allowed,
                })

            # Each tool result must remain linked to its tool_use request.
            self.history.append({"role": "user", "content": results})

        return "Stopped after reaching the step limit."
