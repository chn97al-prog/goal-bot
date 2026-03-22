import requests
import time
from datetime import datetime

BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "@your_channel"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

print("Bot started at:", datetime.now())

while True:
    send_message(f"✅ Bot is alive\n⏰ {datetime.now()}")
    time.sleep(3)
