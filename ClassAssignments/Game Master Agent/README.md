

# 🧙 Game Master Agent

Text-based fantasy adventure game using:

- **NarratorAgent**: Tells story (`generate_event()`)
- **MonsterAgent**: Simulates combat (`roll_dice()`)
- **ItemAgent**: Gives magical rewards

## 🔁 Flow
Turn loop → Narration → Combat → Reward → Repeat

## 🛠️ Tech
- Agent SDK + Runner
- Tools: `roll_dice()`, `generate_event()`

## ▶️ Run
```bash
uv run main.py
