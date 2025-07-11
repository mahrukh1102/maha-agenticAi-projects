from agents import function_tool
import random

@function_tool
def roll_dice(sides: int = 6) -> str:
    result = random.randint(1, sides)
    return f"You rolled a {result} on a {sides}-sided dice."

@function_tool
def generate_event() -> str:
    events = [
        "You enter a dark cave and hear growling.",
        "A hidden treasure chest glows in the forest.",
        "You are ambushed by goblins!",
        "You meet a mysterious traveler who offers help.",
        "You find a magical sword embedded in stone."
    ]
    return random.choice(events)
