import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Load API key from .env
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_ai_suggestions(code, errors):
    prompt = f"Code:\n{code}\n\nErrors:\n{errors}\n\nProvide suggestions to fix these errors."
    response = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
    )
    if response.status_code == 200:
        data = response.json()
        return [candidate["content"]["parts"][0]["text"] for candidate in data.get("candidates", [])]
    return []

def apply_quick_fix(code):
    prompt = f"Code:\n{code}\n\nFix all errors in this code and return the corrected version."
    response = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
    )
    if response.status_code == 200:
        data = response.json()
        fixed_code = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return fixed_code.strip() or code  # Return original code if no fix is found
    return code