import json
from agents.tool import function_tool as tool
from core.grok_client import ask_grok


@tool
async def generate_subject_line(params: str) -> str:
    """
    Generate a subject line for the email.
    Expected JSON format: {"follow_up_email": <str>, "outline": <str> (optional)}
    """
    data = json.loads(params)
    follow_up_email = data.get("follow_up_email", "")
    outline = data.get("outline", "")

    prompt = f"""
You are an expert at writing email subject lines. Based on the follow-up email below,
and optionally the outline provided, generate a compelling, succinct subject line.
Follow-up Email: {follow_up_email}
"""
    if outline:
        prompt += f"\nOutline: {outline}\n"

    prompt += "\nOutput only a single line subject."
    subject_line = await ask_grok([{"role": "user", "content": prompt.strip()}])
    return subject_line
