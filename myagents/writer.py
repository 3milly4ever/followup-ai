import json
from agents.tool import function_tool as tool
from core.grok_client import ask_grok


@tool
async def generate_follow_up(params: str) -> str:
    """
    Generate a follow-up email.
    Expected JSON format: {
       "last_email": <str>,
       "context": <str>,
       "tone": <str>,
       "outline": <str> (optional)
    }
    """
    data = json.loads(params)
    last_email = data.get("last_email", "")
    context = data.get("context", "")
    tone = data.get("tone", "friendly")
    outline = data.get("outline", "")

    prompt = f"""
You are an expert email assistant. Draft a follow-up email with the details provided below.
Last Email: {last_email}
Context: {context}
Tone: {tone.capitalize()}
"""
    if outline:
        prompt += f"\nUse these key points as guidance: {outline}\n"

    prompt += """
Please generate a concise, professional follow-up email body without any extra commentary.
"""
    email = await ask_grok([{"role": "user", "content": prompt.strip()}])
    return email
