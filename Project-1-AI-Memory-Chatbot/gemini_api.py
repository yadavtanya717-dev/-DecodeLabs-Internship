from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def get_response(message, history=None):
    """
    Generate an AI response using Gemini with conversation history.
    """

    if history is None:
        history = []

    # Build conversation prompt
    prompt = ""

    for chat in history:
        prompt += f"{chat['role']}: {chat['content']}\n"

    prompt += f"user: {message}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        error = str(e)

        # Daily quota exceeded
        if "RESOURCE_EXHAUSTED" in error or "429" in error:
            return (
                "⚠️ The daily usage limit for this application has been reached.\n\n"
                "Please try again later."
            )

        # Invalid or missing API Key
        elif (
            "API_KEY" in error
            or "authentication" in error.lower()
            or "permission" in error.lower()
        ):
            return (
                "⚠️ Unable to authenticate the application.\n\n"
                "Please contact the administrator."
            )

        # Internet / Network issue
        elif (
            "connection" in error.lower()
            or "network" in error.lower()
            or "timeout" in error.lower()
        ):
            return (
                "🌐 Unable to connect to the AI service.\n\n"
                "Please check your internet connection and try again."
            )

        # Any other unexpected error
        return (
            "❌ Something went wrong while processing your request.\n\n"
            "Please try again later."
        )