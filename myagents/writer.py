import json
from agents.tool import function_tool as tool
from core.grok_client import ask_grok


@tool
async def generate_follow_up(params: str) -> str:
    """
    Generate a follow-up email based on JSON-encoded parameters.
    Expected JSON format: {"last_email": <str>, "context": <str>, "tone": <str>}
    """
    data = json.loads(params)
    last_email = data.get("last_email", "")
    context = data.get("context", "")
    tone = data.get("tone", "friendly")

    prompt = f"""
You are an expert email assistant who helps busy professionals send effective follow-up emails.

Last Email:
{last_email}

Context:
{context}

Desired Tone: {tone.capitalize()}

Please generate a follow-up email that is concise, professional, and matches the desired tone.
Output only the email body text without any additional commentary.
"""
    return await ask_grok([{"role": "user", "content": prompt.strip()}])
