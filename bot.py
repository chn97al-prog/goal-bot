import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# ================== State ==================
user_state = {}

# ================== Telegram ==================

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def send_photo(chat_id, photo_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    requests.post(url, json={"chat_id": chat_id, "photo": photo_url})

# ================== OpenAI Chat ==================

def ask_ai(prompt):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json()

    return result["choices"][0]["message"]["content"]

# ================== Generate Image ==================

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
    result = res.json()

    if "data" not in result:
        raise Exception(result)

    return result["data"][0]["url"]

# ================== Download Telegram File ==================

def download_telegram_file(file_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    res = requests.get(url, params={"file_id": file_id}).json()

    file_path = res["result"]["file_path"]

    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    file_data = requests.get(file_url)

    file_name = "temp.png"
    with open(file_name, "wb") as f:
        f.write(file_data.content)

    return file_name

# ================== Edit Image ==================

def edit_image(image_path, prompt):
    url = "https://api.openai.com/v1/images/edits"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    files = {
        "image": open(image_path, "rb")
    }

    data = {
        "model": "gpt-image-1",
        "prompt": prompt
    }

    res = requests.post(url, headers=headers, files=files, data=data)
    result = res.json()

    if "data" not in result:
        raise Exception(result)

    return result["data"][0]["url"]

# ================== Webhook ==================

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "no data", 400

    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]

        text = msg.get("text")
        photo = msg.get("photo")

        state = user_state.get(chat_id, "chat")

        # ================= Commands =================

        if text == "/start":
            user_state[chat_id] = "chat"
            send_message(chat_id,
                "👋 أهلاً بك\n\n"
                "الأوامر:\n"
                "/chat - محادثة\n"
                "/generate - إنشاء صورة\n"
                "/edit - تعديل صورة"
            )
            return "ok"

        elif text == "/chat":
            user_state[chat_id] = "chat"
            send_message(chat_id, "💬 وضع المحادثة مفعل")
            return "ok"

        elif text == "/generate":
            user_state[chat_id] = "generate"
            send_message(chat_id, "🎨 أرسل وصف الصورة")
            return "ok"

        elif text == "/edit":
            user_state[chat_id] = "edit"
            send_message(chat_id, "🖼️ أرسل صورة مع وصف (caption)")
            return "ok"

        # ================= Image Edit =================

        elif photo and state == "edit":
            send_message(chat_id, "⏳ جاري تعديل الصورة...")

            try:
                file_id = photo[-1]["file_id"]
                image_path = download_telegram_file(file_id)

                prompt = msg.get("caption", "Edit this image")

                edited_url = edit_image(image_path, prompt)

                send_photo(chat_id, edited_url)

            except Exception as e:
                print(e)
                send_message(chat_id, "❌ فشل تعديل الصورة")

        # ================= Generate =================

        elif text and state == "generate":
            send_message(chat_id, "⏳ جاري إنشاء الصورة...")

            try:
                img = generate_image(text)
                send_photo(chat_id, img)
            except Exception as e:
                print(e)
                send_message(chat_id, "❌ فشل إنشاء الصورة")

        # ================= Chat =================

        elif text:
            if state == "chat":
                send_message(chat_id, "⏳ ...")
                try:
                    reply = ask_ai(text)
                    send_message(chat_id, reply)
                except Exception as e:
                    print(e)
                    send_message(chat_id, "❌ خطأ في AI")

    return "ok", 200

# ================= Home =================

@app.route("/")
def home():
    return "Bot is running"

# ================= Run =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
