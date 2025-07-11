import os
from dotenv import load_dotenv
import chainlit as cl
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    set_default_openai_client,
    set_tracing_disabled
)
from roadmap_tool import get_career_roadmap

# Load environment variables
load_dotenv()

# Configure Gemini
external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
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
        "You assist users in discovering career fields that align with their interests.\n"
        "Examples:\n"
        "- 'I like coding' → 'software engineer'\n"
        "- 'I like design' → 'graphic designer'\n"
        "ONLY suggest one career field. Don't list skills or jobs."
    ),
    model=model
)

skill_agent = Agent(
    name="skill_agent",
    instructions="You provide a skill roadmap using `get_career_roadmap()`.",
    tools=[get_career_roadmap],
    model=model
)

job_agent = Agent(
    name="job_agent",
    instructions="List real-world job titles for a given career field. E.g., 'Software Engineer' → Frontend, Backend, DevOps.",
    model=model
)

# Orchestrator Agent
main_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a career mentor agent. You must follow these steps in this exact order:\n\n"
        "1. Send the user's input to `recommend_career`\n"
        "2. Send the result to `show_skill_roadmap`\n"
        "3. Send the same result to `list_jobs`\n\n"
        "Return the result like this:\n\n"
        "Career Path: <career>\n\n"
        "Required Skills:\n<skills>\n\n"
        "Job Roles:\n<job list>\n\n"
        "RULES:\n"
        "- Do NOT generate anything yourself.\n"
        "- ALWAYS call the 3 tools.\n"
        "- Reply using exact format."
    ),
    tools=[
        career_agent.as_tool("recommend_career", "Suggest a career field"),
        skill_agent.as_tool("show_skill_roadmap", "Show skills"),
        job_agent.as_tool("list_jobs", "List job roles"),
    ],
    model=model
)

# Chat Start
@cl.on_chat_start
async def start():
    await cl.Message(
        content="""
🎓 **Welcome to Career Mentor Agent!**

I'm here to help you discover the perfect career based on your interests or strengths.

Try asking:
- I like solving problems and building apps.
- I'm interested in design and creativity.

Just tell me what you're into!
"""
    ).send()

# Message Handling
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content

    result = await Runner.run(main_agent, user_input)

    await cl.Message(content=result.final_output).send()
