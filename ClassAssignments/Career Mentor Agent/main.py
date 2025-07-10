import os
from dotenv import load_dotenv
import asyncio
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    set_default_openai_client,
    set_tracing_disabled
)
from roadmap_tool import get_career_roadmap


# Config
load_dotenv()
external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),# Replace this if using .env
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

set_default_openai_client(external_client)
set_tracing_disabled(True)

# Agents

career_agent = Agent(
    name="career_agent",
    instructions=(
        "You help students choose careers based on their interests.\n"
        "Examples:\n"
        "- If user says 'I like coding', suggest 'software engineer'\n"
        "- If user says 'I like design', suggest 'graphic designer'\n"
        "- Don't list skills or jobs. Just suggest one career field."
    ),
    model=model
)

skill_agent = Agent(
    name="skill_agent",
    instructions=(
        "You provide skill roadmaps for careers. Use the `get_career_roadmap()` tool."
    ),
    tools=[get_career_roadmap],
    model=model
)

job_agent = Agent(
    name="job_agent",
    instructions=(
        "You list real-world job titles for a given career field.\n"
        "Example for 'software engineer': Frontend Dev, Backend Dev, DevOps."
    ),
    model=model
)

# Orchestrator

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a career mentor agent. You must follow these steps in this exact order:\n\n"
        "1. Take the user's message (like 'I like design') and pass it to the `recommend_career` tool.\n"
        "2. Use the result (e.g. 'graphic designer') as input to `show_skill_roadmap`.\n"
        "3. Use the same result as input to `list_jobs`.\n"
        "4. Combine the 3 outputs into this response format:\n\n"
        "Career Path: <career>\n\n"
        "Required Skills:\n<list of skills>\n\n"
        "Job Roles:\n<list of job roles>\n\n"
        "RULES:\n"
        "- DO NOT generate any response on your own.\n"
        "- ALWAYS call all 3 tools.\n"
        "- Return final output in exact format with spacing and line breaks.\n"
        # "- DO NOT include extra commentary or explanations."
    ),
    tools=[
        career_agent.as_tool("recommend_career", "Suggest a career field"),
        skill_agent.as_tool("show_skill_roadmap", "Display required skills"),
        job_agent.as_tool("list_jobs", "List job roles for a field"),
    ],
    model=model
)

# Run
async def main():
    msg = input("Hi! Tell me your interest or what you're good at: ")

    result = await Runner.run(orchestrator_agent, msg)
    print("\nResponse:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())