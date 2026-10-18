"""Structured output and conversation-history helpers for Lesson 6."""

import json

from claude_assist.prompts import extract_fields_prompt

def parse_json(raw):
    """Parse a JSON string safely and return either data or an error object."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "invalid JSON",
            "raw": raw,
        }
        
        
def extract_fields(client, model, text):
    """Ask Claude for named JSON fields and parse the response safely."""
    prompt = extract_fields_prompt(text)

    resp = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    raw = "".join(block.text for block in resp.content if block.type == "text")
    return parse_json(raw)


def trim_history(messages, n=10):
    """Keep only the most recent n messages."""
    return messages[-n:]