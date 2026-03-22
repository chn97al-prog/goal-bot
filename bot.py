import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def send_photo(chat_id, photo_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(url, json={"chat_id": chat_id, "photo": photo_url})

def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024"
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["data"][0]["url"]

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "👋 اكتب أي وصف وسأحولها لصورة 🎨")
        else:
            send_message(chat_id, "⏳ جاري إنشاء الصورة...")
            try:
                img_url = generate_image(text)
                send_photo(chat_id, img_url)
            except:
                send_message(chat_id, "❌ فشل إنشاء الصورة")

    return "ok"

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
