from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("ANTHROPIC_API_KEY")

print("Environment ready" if key else "Missing")