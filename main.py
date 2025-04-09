import sys
import os
import asyncio
import json

# Add the SDK src folder to Python's sys.path.
sys.path.insert(0, os.path.join(os.getcwd(), "openai-agents-python", "src"))

# Set up the default client for Grok (we use the SDK’s functions from its "agents" package)
from agents import (
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from openai import AsyncOpenAI

# Initialize the Grok client with your API key and base URL.
client = AsyncOpenAI(
    base_url="https://api.x.ai/v1",
    api_key="xai-P2Sd3AcIvvA2FO9UBcZHtQulOKKTOyQSu2OodtqLUVzywCisd8X6rjZ1oygbkhiozNPwvqEyuidPcLQ2",
)
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

# Now import the Agent and Runner from the SDK.
from agents import Agent
from agents.run import Runner

# Import your follow-up email generation tool from your local folder.
from myagents.writer import generate_follow_up


async def main(last_email: str, context: str, tone: str):
    followup_agent = Agent(
        name="FollowUpWriter",
        instructions="You are a helpful assistant that writes concise, professional follow-up emails.",
        tools=[generate_follow_up],
        model="grok-2-1212",
    )

    # Prepare the input as a list with one message item.
    # The message is a dict with "role" and "content" where the content is a JSON string.
    input_data = [
        {
            "role": "user",
            "content": json.dumps(
                {"last_email": last_email, "context": context, "tone": tone}
            ),
        }
    ]

    result = await Runner.run(
        starting_agent=followup_agent, input=input_data, context={}
    )

    print("\n--- Generated Follow-Up Email ---")
    print(result.final_output)


if __name__ == "__main__":
    last_email = input("Enter the last email: ")
    context = input("Enter additional context: ")
    tone = input("Enter desired tone (friendly, assertive, curious): ")

    asyncio.run(main(last_email, context, tone))
