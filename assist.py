from dotenv import load_dotenv

from claude_assist import config
from claude_assist.conversation import Conversation


# Load the API key from the .env file.
load_dotenv()

# Create one Conversation object for the whole chat.
convo = Conversation(config.SYSTEM)

while True:
    user = input("You: ")

    if user.lower() == "quit":
        break

    print("Claude:", convo.send(user))
