import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


def generate_answer(prompt):
    """
    Sends the prompt to Gemini and returns the generated response.

    Args:
        prompt (str): Prompt containing retrieved context and user question.

    Returns:
        str: Generated answer.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except ServerError:
        return (
            "Gemini is currently experiencing high demand. "
            "Please try again in a few minutes."
        )

    except Exception as error:
        return f"Unexpected Error: {error}"