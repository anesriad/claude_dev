# Lesson 20: Run the completed Claude Assist CLI using the existing Conversation and agent.
# Commands: chat for conversation, agent for a multi-step task, notes to read saved briefs.

from claude_assist import config
from claude_assist.conversation import Conversation
from claude_assist.agent import run_agent
from claude_assist.mcp_notes import call_note_tool

# Show the available commands when the application starts.
def show_help():
    print("\nClaude Assist v1.0 | Meeting & Project Briefing Assistant")
    print("Commands: chat, agent, notes, help, quit")
    print("  chat  - talk to Claude and keep conversation history")
    print("  agent - run a multi-step task using tools and MCP")
    print("  notes - read the last saved briefs\n")

# Run the interactive assistant until the user chooses to quit.
def main():
    # Check the key once before starting a paid Claude session.
    config.require_api_key()
    conversation = Conversation(config.SYSTEM)
    previous_user_facts = []
    show_help()

    while True:
        command = input("Choose [chat/agent/notes/help/quit]: ").strip().lower()
        if command in ("quit", "exit", "q"):
            print("Session closed.")
            break
        if command == "help":
            show_help()
        elif command == "chat":
            text = input("You: ")
            answer = conversation.send(text)
            print("Claude:", answer)
            # Pass only successfully checked, prior user context to the agent.
            if not answer.startswith(("Input rejected:", "Response blocked:", "Stopped:")):
                previous_user_facts.append(text)
                previous_user_facts = previous_user_facts[-3:]
        elif command == "agent":
            goal = input("Task: ")
            context = "\n".join(previous_user_facts)
            try:
                result = run_agent(goal, return_trace=True, context=context)
                print("\nClaude:", result["answer"])
                print("Tools used:", result["tools_used"])
                print("Steps:", result["steps"])
                if result["blocked_tools"]:
                    print("Blocked/failed:", result["blocked_tools"])
            except Exception as error:
                print(f"Request failed ({type(error).__name__}). Check your connection or settings.")
        elif command == "notes":
            try:
                print("Saved notes:", call_note_tool("get_notes", {}))
            except Exception as error:
                print(f"Could not read notes ({type(error).__name__}).")
        else:
            print("Unknown command. Enter help to see the options.")

# Only start the interactive CLI when this file is run directly.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSession closed.")
    except RuntimeError as error:
        print("Setup error:", error)
