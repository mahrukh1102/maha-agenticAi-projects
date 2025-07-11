# 🎓 Career Mentor Agent

Helps users find suitable careers by coordinating:

- **CareerAgent**: Suggests a career path
- **SkillAgent**: Lists required skills (via `get_career_roadmap()`)
- **JobAgent**: Suggests related job roles

## 🔁 Flow
User input → CareerAgent → SkillAgent → JobAgent → Final response

## 🛠️ Tech
- OpenAI Agent SDK + Runner
- Tool: `get_career_roadmap()`

## ▶️ Run
```bash
uv run main.py
