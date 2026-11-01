import anthropic

from claude_assist import config
from claude_assist.tools import TOOL_DEFINITIONS, dispatch


class Conversation:
    # Set up the Claude client, system prompt, and empty history.
    def __init__(self, system):
        self.client = anthropic.Anthropic()
        self.system = system
        self.history = []

    # Send one message and keep handling tools until Claude gives a final answer.
    def send(self, text):
        if not text.strip():
            return "Please enter a message."

        self.history.append({
            "role": "user",
            "content": text
        })

        while True:
            resp = self.client.messages.create(
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                system=self.system,
                tools=TOOL_DEFINITIONS,
                messages=self.history
            )

            # Keep Claude's response in the conversation history.
            self.history.append({
                "role": "assistant",
                "content": resp.content
            })

            # If Claude is finished, return the final answer.
            if resp.stop_reason != "tool_use":
                for block in resp.content:
                    if block.type == "text":
                        return block.text

                return "Claude finished without a text response."

            results = []

            # Run every tool Claude requested in this response.
            for block in resp.content:
                if block.type == "tool_use":
                    result = dispatch(
                        block.name,
                        block.input
                    )

                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            # Return all tool results together before the next Claude call.
            self.history.append({
                "role": "user",
                "content": results
            })
