from agents import function_tool as tool
from core.grok_client import ask_grok


@tool
async def generate_follow_up(last_email: str, context: str, tone: str) -> str:
    """
    Generate a follow-up email based on the last email, additional context,
    and the selected tone (e.g., "friendly", "assertive", "curious").

    Returns only the email body as plain text.
    """
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
    # Call the Grok API via your grok_client
    return await ask_grok([{"role": "user", "content": prompt.strip()}])
