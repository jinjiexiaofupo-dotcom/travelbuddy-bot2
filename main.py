import os
from flask import Flask, request
from openai import OpenAI
from telegram import Bot

# 从环境变量读取
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

app = Flask(__name__)

SYSTEM_PROMPT = """
You are TravelBuddy, a playful English tutor for an ENFP learner.
Run short daily adventures (10–15 mins).
Correct mistakes gently, offer one natural alternative phrase,
and end each session with a fun badge/points summary.
"""

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        user_input = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300
        )
        reply = response.choices[0].message.content
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok", 200
