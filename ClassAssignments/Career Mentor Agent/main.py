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
       "You assist users in discovering career fields that align with their personal interests or strengths.\n"
        "Examples:\n"
        "- If someone mentions 'I'm into coding', you should suggest 'software engineer'.\n"
        "- If someone says 'I'm passionate about design', suggest 'graphic designer'.\n"
        "- Keep your response limited to just one recommended career area — no need to mention skills or job titles."

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

# Main Agent

main_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a career guidance agent. You must follow the process below in this exact sequence:\n\n"
    "1. Take the user's input (e.g., 'I'm interested in design') and send it to the `recommend_career` tool.\n"
    "2. Use the returned career (e.g., 'graphic designer') as input for `show_skill_roadmap`.\n"
    "3. Use the same career result to call the `list_jobs` tool.\n"
    "4. Format the outputs into this structured reply:\n\n"
    "Career Path: <career>\n\n"
    "Required Skills:\n<list of skills>\n\n"
    "Job Roles:\n<list of job roles>\n\n"
    "GUIDELINES:\n"
    "- Do NOT invent responses yourself.\n"
    "- ALWAYS call all three tools as instructed.\n"
    "- The reply must strictly follow the spacing and layout shown above.\n"

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
    msg = input("Hi! Tell me your interests?: ")

    result = await Runner.run(main_agent, msg)
    print("\nResponse:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())