# Claude Assist

A small Claude-powered assistant built during the Claude Certified Developer Foundations course. It supports conversation history, local tools, an MCP notes tool, a bounded agent loop, guardrails, and request monitoring.

## Setup

1. Create and activate a Python virtual environment.
2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` with your own key. Keep `.env` out of Git.

## Run the assistant

```bash
python assist.py
```

## Run the agent

From the project root, with your key configured:

```python
from claude_assist.agent import run_agent

print(run_agent("Prepare a short client-call note, count its words, then save it."))
```

The agent can use `get_time`, `count_words`, `calculate`, and the MCP `save_note` tool. The notes server is local and notes are stored in memory for this course.

## Check the project

Run the offline integration checks first (no real key/API call needed):

```bash
python integration_check.py
pytest tests/test_integration.py -q
```

Then run existing tests and model evaluations when ready:

```bash
pytest -q
python run_evals.py
```

The evaluations call Claude and may use API credits. The full live capstone demonstration is in Lesson 20.

## Main files

- `claude_assist/agent.py`: agent loop with tools and guardrails
- `claude_assist/conversation.py`: conversation history and request hooks
- `claude_assist/config.py`: settings and API key checks
- `claude_assist/tools.py`: local tools and dispatcher
- `mcp_server.py`: local MCP notes server
- `evals/` and `tests/`: quality checks
- `integration_check.py`: Lesson 19 offline integration checks

## Safety

Do not commit `.env`, credentials, or private user content. Verify that `.env` is ignored **and not tracked** before tagging a release candidate.
