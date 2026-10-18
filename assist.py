import anthropic
from dotenv import load_dotenv

from claude_assist.config import MODEL, MAX_TOKENS, SYSTEM


# Load the API key from the .env file.
load_dotenv()

# Create the Claude API client.
client = anthropic.Anthropic()

# Ask the user for one message.
user_text = input("You: ")

# Send the message to Claude.
resp = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    system=SYSTEM,
    messages=[
        {"role": "user", "content": user_text}
    ]
)

# Print Claude's reply.
print("Claude:", resp.content[0].text)