import sys
import os
import asyncio
import json

# Add the SDK src folder to sys.path
sys.path.insert(0, os.path.join(os.getcwd(), "openai-agents-python", "src"))

# --- Set up default client for Grok ---
from agents import (
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.getenv("GROK_API_KEY", "your_fallback_api_key_here"),
)
set_default_openai_client(client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)
# --- End client setup ---

# Import SDK classes
from agents import Agent
from agents.run import Runner

# Import your agent tools from your myagents folder
from myagents.planner import plan_email
from myagents.writer import generate_follow_up

# (Later you can import subject and refiner agents as needed)


async def main(last_email: str, context: str, tone: str):
    # 1. Run the Planner Agent to get an outline.
    planner_agent = Agent(
        name="EmailPlanner",
        instructions="Generate a concise outline of key points to cover in a follow-up email.",
        tools=[plan_email],
        model="grok-2-1212",
    )

    planner_input = [
        {
            "role": "user",
            "content": json.dumps(
                {"last_email": last_email, "context": context, "tone": tone}
            ),
        }
    ]

    planner_result = await Runner.run(
        starting_agent=planner_agent, input=planner_input, context={}
    )
    outline = planner_result.final_output.strip()
    print("\n--- Outline from Planner Agent ---")
    print(outline)

    # 2. Run the Writer Agent, including the outline in the input.
    writer_agent = Agent(
        name="FollowUpWriter",
        instructions="Using the given outline, draft a concise follow-up email.",
        tools=[generate_follow_up],
        model="grok-2-1212",
    )

    writer_input = [
        {
            "role": "user",
            "content": json.dumps(
                {
                    "last_email": last_email,
                    "context": context,
                    "tone": tone,
                    "outline": outline,
                }
            ),
        }
    ]

    writer_result = await Runner.run(
        starting_agent=writer_agent, input=writer_input, context={}
    )
    follow_up_email = writer_result.final_output.strip()
    print("\n--- Generated Follow-Up Email ---")
    print(follow_up_email)

    # Future Steps: You would run the Subject Line and Refinement Agents here,
    # passing follow_up_email and optionally the outline to get a subject line and refined content.


if __name__ == "__main__":
    last_email = input("Enter the last email: ")
    context = input("Enter additional context: ")
    tone = input("Enter desired tone (friendly, assertive, curious): ")

    asyncio.run(main(last_email, context, tone))
