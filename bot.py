import requests
import time
from datetime import datetime

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "@Gol_lives"

API_URL = "https://www.scorebat.com/video-api/v3/"

posted_matches = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        })
    except:
        pass

def get_matches():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        return data.get("response", [])
    except:
        return []

print("Bot started:", datetime.now())

while True:
    matches = get_matches()
    leagues = {}

    for m in matches:
        title = m.get("title")

        # ✅ معالجة competition بشكل آمن
        competition = m.get("competition")

        if isinstance(competition, dict):
            comp = competition.get("name", "Unknown League")
        else:
            comp = "Unknown League"

        url = m.get("url")

        if not title or not url:
            continue

        key = title + str(url)

        if key not in posted_matches:
            if comp not in leagues:
                leagues[comp] = []

            leagues[comp].append((title, url))
            posted_matches.add(key)

    # 📤 إرسال لكل دوري
    for league, games in leagues.items():
        message = f"🏆 {league}\n"
        message += "━━━━━━━━━━━━━━\n\n"

        for title, url in games:
            message += f"⚽ {title}\n🎥 {url}\n\n"

        message += f"⏰ {datetime.now()}"

        send_message(message)
        time.sleep(2)

    time.sleep(300)
