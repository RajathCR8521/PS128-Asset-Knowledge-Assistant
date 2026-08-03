import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Running NEW test_gemini.py")

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Say hello in one sentence."
    )

    print(response.text)

except ServerError:
    print("⚠️ Gemini servers are currently busy (503). Please try again after a few minutes.")

except Exception as e:
    print(f"Unexpected error: {e}")