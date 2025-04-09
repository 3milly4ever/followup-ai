import json
from agents.tool import function_tool as tool
from core.grok_client import ask_grok


@tool
async def plan_email(params: str) -> str:
    """
    Generate an outline for the follow-up email.
    Expected JSON format: {"last_email": <str>, "context": <str>, "tone": <str>}
    Output: A bullet-list (one per line) of key points that the follow-up email should cover.
    """
    data = json.loads(params)
    last_email = data.get("last_email", "")
    context = data.get("context", "")
    tone = data.get("tone", "friendly")

    prompt = f"""
You are an expert email strategist. Analyze the following details and generate an outline 
(with bullet points, one per line) of key points that a follow-up email should cover.

Last Email:
{last_email}

Context:
{context}

Tone: {tone.capitalize()}

Output only the bullet-list outline.
"""
    outline = await ask_grok([{"role": "user", "content": prompt.strip()}])
    return outline
