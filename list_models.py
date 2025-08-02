import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Make sure your .env has GOOGLE_API_KEY

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
