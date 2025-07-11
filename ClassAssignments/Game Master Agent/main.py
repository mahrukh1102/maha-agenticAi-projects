import os
from dotenv import load_dotenv
import time
import asyncio
from game_tools import roll_dice, generate_event
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Agent,
    Runner,
    set_default_openai_client,
    set_tracing_disabled
)


# Config
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


#  Agents

narrator_agent = Agent(
    name="narrator_agent",
    instructions="You narrate the adventure. Use `generate_event` to describe what happens next.",
    tools=[generate_event],
    model=model
)

monster_agent = Agent(
    name="monster_agent",
    instructions="You simulate a battle. Use `roll_dice` to determine fight outcomes. Always explain results.",
    tools=[roll_dice],
    model=model
)

item_agent = Agent(
    name="item_agent",
    instructions="You reward the player with a magical item. Be creative.",
    model=model
)


#Main_Agent

main_agent = Agent(
    name="main_agent",
    instructions=(
    "You are the Game Master in a fantasy RPG.\n\n"
    "Each turn must follow these steps:\n"
    "1. Call the `narrate_event` tool to generate a story event.\n"
    "2. Call the `combat_phase` tool to simulate a battle.\n"
    "3. Call the `reward_item` tool to give a magical item.\n\n"
    "You MUST use each tool exactly once per turn.\n"
    "DO NOT make up any of this yourself. Use the tools only.\n"
    "Return the results in this exact format:\n\n"
    "📖 Story:\n{narration result}\n\n"
    "⚔️ Combat:\n{combat result}\n\n"
    "🎁 Reward:\n{item result}\n"
),

    tools=[
        narrator_agent.as_tool("narrate_event", "Describe an adventure scenario"),
        monster_agent.as_tool("combat_phase", "Resolve combat using dice"),
        item_agent.as_tool("reward_item", "Give magical item reward")
    ],
    model=model
)

#  Game Loop
async def main():
    name = input("Enter your adventurer's name: ")
    print(f"\nWelcome, {name}! Your fantasy journey begins...\n")

    keep_playing = True
    while keep_playing:
        result = await Runner.run(main_agent, f"Continue {name}'s journey.")
        print("\n" + result.final_output)

        #  Wait before next turn to avoid rate limit
        import time
        time.sleep(30)

        choice = input("\n🎮 Continue playing? (yes/no): ").strip().lower()
        if choice != "yes":
            keep_playing = False
            print("\n🏁 The journey ends here. Until next time, adventurer!")

if __name__ == "__main__":
    asyncio.run(main())



