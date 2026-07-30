from flask import Flask, render_template, request, jsonify
with open(".env", "r") as f:
    print("Raw .env contents:")
    print(repr(f.read()))
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import certifi

app = Flask(__name__)

env_path = Path(__file__).parent / ".env"
print("Loading:", env_path)

load_dotenv(dotenv_path=env_path)

from dotenv import dotenv_values

config = dotenv_values(".env")
print("CONFIG:", config)

API_KEY = config.get("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")
print("API KEY:", API_KEY)
MODEL = "deepseek/deepseek-chat-v3-0324:free"



SYSTEM_PROMPT = """
You are Chaos N Giggle.

Personality:
- Funny
- Energetic
- Smart
- Friendly
- Loves jokes, memes, games and stories.
- Keep replies natural.
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
                "Content-Type":"application/json"
            },

            json={

                "model": MODEL,

                "messages":[

                    {
                        "role":"system",
                        "content":SYSTEM_PROMPT
                    },

                    {
                        "role":"user",
                        "content":user
                    }

                ]

            },

            timeout=60,
            verify=certifi.where()

        )

        print("="*50)
        print("STATUS:", response.status_code)
        print(response.text)
        print("="*50)

        if response.status_code != 200:

            return jsonify({
                "reply": f"OpenRouter Error ({response.status_code})"
            })

        data = response.json()

        reply = data["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({
            "reply": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)