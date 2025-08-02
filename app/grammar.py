import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("enter_your_google_api_secret_key_here")
genai.configure(api_key=api_key)

def correct_grammar(text: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Please correct the grammar of the following sentence:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during grammar correction: {e}"
