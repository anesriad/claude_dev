"""Reusable prompt templates for Lesson 5."""

"""Return a simple prompt for a one-sentence summary."""
def summarize_prompt(text):
    return f"""You are a concise editor.

Summarise the text below in one clear sentence.

<text>
{text} 
</text>

Return only the summary."""


"""Return a stronger prompt that answers only from supplied context."""
def answer_with_context(question, context):
    return f"""You are a careful research assistant.

Answer the question using only the context provided below.

<context>
{context}
</context>

<question>
{question}
</question>

Requirements:
- Use only information supported by the context.
- If the context does not contain enough information, say that clearly.
- Keep the answer concise and directly relevant.

Return only the final answer."""


"""Return a prompt that requests a small JSON object with named fields."""
def extract_fields_prompt(text):
    return f"""Extract the key information from the text below.

Return ONLY valid JSON with exactly these keys:
- "name"
- "topic"

<text>
{text}
</text>

Do not include markdown, code fences, or any text outside the JSON object."""