from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import certifi

app = Flask(__name__)

env_path = Path(__file__).parent / ".env"
print("Loading:", env_path)

load_dotenv(dotenv_path=env_path)

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

print(API_KEY)
MODEL = "moonshotai/kimi-k2:"


SYSTEM_PROMPT = """
You are Chaos N Giggle.

Personality:
- Funny
- Energetic
- Smart
- Friendly
- Loves jokes, memes, games and stories.
- Keep replies natural and short.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user = request.json["message"]

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user
                    }
                ],
                "max_tokens": 512,
                "temperature": 0.8
            },
            timeout=60,
            verify=certifi.where()
        )

        print("=" * 50)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("=" * 50)

        if response.status_code != 200:
            return jsonify({
                "reply": response.text
            })

        data = response.json()

        return jsonify({
            "reply": data["choices"][0]["message"]["content"]
        })

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({
            "reply": str(e)
        })
if __name__ == "__main__":
    print("Starting Flask...")
    app.run(debug=True)
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)