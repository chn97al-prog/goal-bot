import requests
import time
from datetime import datetime

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "@Gol_lives"

API_URL = "https://www.scorebat.com/video-api/v3/"

posted_matches = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def get_matches():
    try:
        r = requests.get(API_URL)
        return r.json().get("response", [])
    except:
        return []

print("Bot started:", datetime.now())

while True:
    matches = get_matches()

    leagues = {}

    # 🧠 تجميع المباريات حسب الدوري
    for m in matches:
        title = m.get("title")
        comp = m.get("competition", {}).get("name", "Unknown League")
        url = m.get("url")

        key = title + str(url)

        if key not in posted_matches:
            if comp not in leagues:
                leagues[comp] = []

            leagues[comp].append((title, url))
            posted_matches.add(key)

    # 📤 إرسال كل دوري برسالة منفصلة
    for league, games in leagues.items():
        message = f"🏆 {league}\n"
        message += "━━━━━━━━━━━━━━\n\n"

        for game in games:
            title, url = game
            message += f"⚽ {title}\n🎥 {url}\n\n"

        message += f"⏰ {datetime.now()}"

        send_message(message)
        time.sleep(2)

    time.sleep(300)
