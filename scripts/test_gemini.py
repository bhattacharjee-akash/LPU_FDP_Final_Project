import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# We load from both backend folder env or local env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

key = os.environ.get("GEMINI_API_KEY")
print(f"Loaded GEMINI_API_KEY prefix: {key[:8] if key else 'None'}...")

if not key:
    print("Error: GEMINI_API_KEY environment variable is not set!")
    exit(1)

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Sending test request to Gemini...")
    response = model.generate_content("Hello! What is your model name?")
    print(f"Gemini API Response: {response.text}")
except Exception as e:
    import traceback
    print("Gemini API call failed with traceback:")
    traceback.print_exc()
