# 🌍 AI Travel Designer Agent

Plans a complete travel experience by coordinating multiple AI agents.

---

## 🧠 What It Does

- Suggests destinations based on mood or interests
- Books flights and finds hotels using mock tools
- Recommends things to do and places to eat

---

## 👤 Agents Involved

- **DestinationAgent** – Recommends travel locations
- **BookingAgent** – Uses `get_flights()` to simulate flight options
- **ExploreAgent** – Uses `suggest_hotels()` to find accommodations and attractions

---

## 🔄 Flow

User Input → DestinationAgent → BookingAgent → ExploreAgent → Final Travel Plan


## 🛠️ Tech Stack

- ✅ OpenAI Agent SDK + Runner
- 🧰 Tools Used:
  - `get_flights()`
  - `suggest_hotels()`


## ▶️ Run

```bash
uv run main.py
