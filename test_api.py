import requests
import os
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "google/gemma-4-26b-a4b-it:free",
        "messages": [{"role": "user", "content": "Say hello in one word"}]
    }
)

print(response.json())