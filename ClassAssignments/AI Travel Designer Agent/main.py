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
from travel_tools import get_flights, suggest_hotels, explore_city

load_dotenv()
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


# Agents

destination_agent = Agent(
    name="destination_agent",
    instructions="You suggest a travel destination based on mood or interests.",
    model=model
)

booking_agent = Agent(
    name="booking_agent",
    instructions="You simulate travel bookings using tools like `get_flights` and `suggest_hotels`.",
    tools=[get_flights, suggest_hotels],
    model=model
)

explore_agent = Agent(
    name="explore_agent",
    instructions="You suggest things to do in a city (attractions, food, culture). Use the `explore_city` tool.",
    tools=[explore_city],
    model=model
)

# Main Agent

main_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are an AI Travel Designer. Always follow this exact 3-step process using the tools below:\n\n"
        "1. Use `recommend_destination` tool on the user's input to get a destination.\n"
        "2. Use that destination with `booking_info` to get mock flight and hotel data.\n"
        "3. Use the same destination with `explore_info` to suggest attractions.\n\n"
        "Return the final output in this format (DO NOT DEVIATE):\n\n"
        "Destination: <destination>\n\n"
        "Flights:\n<flight info>\n\n"
        "Hotels:\n<hotel info>\n\n"
        "Attractions:\n<explore info>\n\n"
        "RULES:\n"
        "- Do NOT ask the user questions.\n"
        "- Do NOT guess anything yourself.\n"
        "- ALWAYS use the tools in exact order.\n"
        "- NEVER skip tools, even if input is vague.\n"
        "- DO NOT generate your own text. Use only tool outputs."
    ),
    tools=[
        destination_agent.as_tool("recommend_destination", "Suggest destination based on mood"),
        booking_agent.as_tool("booking_info", "Get flights and hotels"),
        explore_agent.as_tool("explore_info", "Attractions and food")
    ],
    model=model
)




# Runner
async def main():
    msg = input("Tell me your travel mood or interest (e.g., 'I want a relaxing beach trip'): ")
    result = await Runner.run(main_agent, msg)
    print("\n Response:\n")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
