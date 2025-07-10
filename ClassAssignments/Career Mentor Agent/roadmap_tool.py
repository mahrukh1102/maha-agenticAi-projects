# from agents import function_tool

# @function_tool
# def get_career_roadmap(field: str) -> str:
#     maps = {
#         "software engineer": "Learn Python, DSA, Web Dev, GitHub, Projects.",
#         "data science": "Master Python, Pandas, ML, and real-world datasets.",
#         "graphic designer": "Learn Figma, Photoshop, UI/UX, Portfolio.",
#         "ai": "Study Python, Deep Learning, Transformers, and AI tools."
#     }
#     return maps.get(field.lower(), "No roadmap found for that field.")



# roadmap_tool.py

# from agents import function_tool

# @function_tool
# def get_career_roadmap(field: str) -> str:
#     """Returns a basic roadmap of skills and tools required to enter the selected career field."""
#     roadmaps = {
#         "software engineer": "1. Learn Python & JavaScript\n2. Understand Data Structures & Algorithms\n3. Build full-stack apps with React and Node.js\n4. Use Git and GitHub\n5. Practice on LeetCode or HackerRank",
#         "data science": "1. Master Python & Pandas\n2. Learn statistics and probability\n3. Get comfortable with SQL\n4. Practice with real-world datasets\n5. Learn machine learning and deep learning frameworks",
#         "graphic designer": "1. Learn Adobe Photoshop & Illustrator\n2. Understand design principles and typography\n3. Build a portfolio with Dribbble or Behance\n4. Learn Figma or Sketch\n5. Understand basic UI/UX concepts",
#         "ai": "1. Learn Python\n2. Study linear algebra, calculus, and probability\n3. Get hands-on with TensorFlow or PyTorch\n4. Work on deep learning projects\n5. Read recent AI research papers",
#         "marketing": "1. Understand digital marketing fundamentals\n2. Learn SEO, SEM, and analytics tools\n3. Practice with Google Ads and Meta Ads\n4. Study copywriting & email marketing\n5. Run your own campaigns for testing"
#     }

#     return roadmaps.get(field.lower(), "Sorry, I don't have a roadmap for that field. Try 'software engineer', 'data science', 'graphic designer', 'ai', or 'marketing'.")


# roadmap_tool.py

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
