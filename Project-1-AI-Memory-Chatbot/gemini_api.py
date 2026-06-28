from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def get_response(message, history=None):
    """
    Generate a response from Gemini using previous conversation memory.
    """

    if history is None:
        history = []

    # Build prompt
    if history:
        prompt = (
            "You are an intelligent AI Memory Chatbot.\n"
            "Use the previous conversation below as context whenever it is relevant.\n\n"
            "Previous Conversation:\n"
        )

        for chat in history:
            role = chat.get("role", "user")
            content = chat.get("content", "")
            prompt += f"{role}: {content}\n"

        prompt += f"\nCurrent User Message:\n{message}"

    else:
        prompt = (
            "You are an intelligent AI assistant.\n"
            "There is no previous conversation history because the memory is empty or has been cleared.\n\n"
            f"Current User Message:\n{message}"
        )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "I couldn't generate a response. Please try again."

    except Exception as e:
        return (
            "⚠️ Sorry, I couldn't contact Gemini right now.\n\n"
            f"Error: {str(e)}"
        )