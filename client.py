from dotenv import load_dotenv
import os
from google import genai

load_dotenv()           
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(command):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=command,
        )
        return response.text
    except Exception as e:
        return f"Sorry, an error occurred: {e}"