import requests
from app.config import OPENROUTER_API_KEY

def call_llm(prompt):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a scientific assistant"},
                {"role": "user", "content": prompt}
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]