import requests
import time
from datetime import datetime

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "@Gol_lives"

# 📡 مصدر مباريات (API مجاني كمثال)
API_URL = "https://www.scorebat.com/video-api/v3/"

# نخزن آخر فيديو حتى ما نكرر
posted_links = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def get_matches():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data.get("response", [])
    except:
        return []

print("Bot started at:", datetime.now())

while True:
    matches = get_matches()

    for match in matches:
        title = match.get("title")
        url = match.get("url")

        # نتأكد ما نشرناه قبل
        if url and url not in posted_links:
            message = f"""⚽ New Match Update

🏆 {title}
🎥 Watch: {url}

⏰ {datetime.now()}"""

            send_message(message)
            posted_links.add(url)

            time.sleep(2)

    time.sleep(60)
