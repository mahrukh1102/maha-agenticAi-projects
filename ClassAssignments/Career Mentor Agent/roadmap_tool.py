

from agents import function_tool

@function_tool
def get_career_roadmap(field: str) -> str:
    roadmaps = {
        "software engineer": "1. Learn Python & JavaScript\n2. DSA\n3. Web Dev (React, Node.js)\n4. GitHub\n5. Projects",
        "data science": "1. Python\n2. Pandas & SQL\n3. ML\n4. Stats\n5. Real-world projects",
        "graphic designer": "1. Adobe Tools\n2. Typography\n3. Portfolio\n4. Figma/UI/UX",
        "ai": "1. Python\n2. DL frameworks (TensorFlow, PyTorch)\n3. NLP, Vision, RL\n4. Projects",
        "marketing": "1. SEO, SEM\n2. Content creation\n3. Google Ads\n4. Social media strategy"
    }
    return roadmaps.get(field.lower(), "Sorry, I don't have a roadmap for that field.")
