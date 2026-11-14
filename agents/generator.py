
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from memory.learning import get_improvement_suggestions

# Load API key from .env file
load_dotenv()

# Create the Gemini AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.3
)

def generate_lesson(topic, feedback=None):

    prompt = f"""
    You are an expert teacher.

    Create a beginner-friendly lesson on: {topic}

    Follow these rules:
    1. Explain the topic in simple English.
    2. Start with the basics.
    3. Explain technical terms.
    4. Include practical examples.
    5. Use headings and clear sections.
    6. Do not include incorrect information.

    """
    # Get improvement suggestions from previous  evaluations
    suggestions = get_improvement_suggestions(topic)

    if suggestions:
        prompt += "\n\nPrevious failure patterns and improvements:\n"

        for suggestion in suggestions:
            prompt += f"- {suggestion}\n"




    if feedback:
        prompt += f"""
        Your previous lesson was rejected.

        Evaluator feedback:
        {feedback}

        Improve the lesson based on this feedback.
        """
    print("Sending request to Gemini...")
    response = llm.invoke(prompt)
    print("Gemini response received..!")

    content = response.content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        return "\n".join(text_parts)

    return content
