from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

import certifi


API_KEY = os.getenv("")
print("API KEY:", API_KEY)

MODEL = "openrouter/auto"



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