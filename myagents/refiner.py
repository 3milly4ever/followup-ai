import json
from agents.tool import function_tool as tool
from core.grok_client import ask_grok


@tool
async def refine_email(params: str) -> str:
    """
    Refine the provided follow-up email.
    Expected JSON format: {"draft_email": <str>}
    """
    data = json.loads(params)
    draft_email = data.get("draft_email", "")

    prompt = f"""
You are an expert editor. Refine and polish the following follow-up email to improve its grammar,
tone, and clarity while keeping the original meaning intact.
Draft Email: {draft_email}
Output only the refined email.
"""
    refined_email = await ask_grok([{"role": "user", "content": prompt.strip()}])
    return refined_email
