import chainlit as cl
import os
from dotenv import load_dotenv
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    set_default_openai_client,
    set_tracing_disabled
)
from roadmap_tool import get_career_roadmap

# Setup Gemini client
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

# Define Agents
career_agent = Agent(
    name="career_agent",
    instructions=(
        "You help suggest a career field based on a user's interest. Only return one job field like 'graphic designer', 'software engineer', etc."
    ),
    model=model
)

skill_agent = Agent(
    name="skill_agent",
    instructions="You show a skill roadmap for the given career field.",
    tools=[get_career_roadmap],
    model=model
)

job_agent = Agent(
    name="job_agent",
    instructions="You list job roles related to the given career field.",
    model=model
)

# Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a career mentor agent. Follow these steps strictly:\n"
        "1. Use `recommend_career` tool on the user's input.\n"
        "2. Use the result (career field) with `show_skill_roadmap`.\n"
        "3. Use same result with `list_jobs`.\n"
        "4. Output format:\n"
        "\n"
        "Career Path: <career>\n\n"
        "Required Skills:\n<skills>\n\n"
        "Job Roles:\n<jobs>\n"
        "Use tools only. Never guess or skip steps."
    ),
    tools=[
        career_agent.as_tool("recommend_career", "Suggest a career field"),
        skill_agent.as_tool("show_skill_roadmap", "Show required skills"),
        job_agent.as_tool("list_jobs", "List job roles"),
    ],
    model=model
)

# Chainlit handler
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    result = await Runner.run(orchestrator_agent, user_input)
    await cl.Message(content=result.final_output).send()
