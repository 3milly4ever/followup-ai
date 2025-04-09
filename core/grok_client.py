from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.getenv("GROK_API_KEY", "fallback_api_key_if_needed"),
)


async def ask_grok(messages: list) -> str:
    response = await client.chat.completions.create(
        model="grok-2-1212",
        messages=messages,
    )
    return response.choices[0].message.content
