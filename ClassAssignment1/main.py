from dotenv import load_dotenv
import os
from agents import Agent , Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # You can change this model version if needed
    openai_client=external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


smartagent = Agent(
    name="Smart Student Assistant",
    instructions="Answer academic questions, provide study tips, and summarize text passages.",
)

# Func to handle academic questions
def academic_q_a(question):
    input_text = f"Answer the following academic question: {question}"
    return Runner.run_sync(smartagent, input=input_text, run_config=config)

# Func to provide study tips
def study_tips(subject):
    input_text = f"Provide study tips for the subject in 2 lines: {subject}"
    return Runner.run_sync(smartagent, input=input_text, run_config=config)

# Func to summarize text
def summarize_text(text):
    input_text = f"Summarize the following text in 2 lines: {text}"
    return Runner.run_sync(smartagent, input=input_text, run_config=config)

#testing 
if __name__ == "__main__":
    # Example academic question
    question = "How many letters in english alphabet?"
    print("Answer to Question:", academic_q_a(question))

    # Example study tips
    subject = "Agentic Ai"
    print("Study Tips:", study_tips(subject))

    # Example text summary
    text = "Agentic AI refers to systems that can autonomously perform tasks, make decisions, and adapt to changing environments. Unlike traditional AI, it can act independently, making real-time decisions. This technology is used in robotics, autonomous vehicles, and virtual assistants. The main challenge with agentic AI is ensuring safety, control, and accountability as it evolves."
    print("Summary:", summarize_text(text))


