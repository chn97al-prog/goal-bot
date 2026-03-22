import requests
import time
from datetime import datetime

# 🔑 ضع توكن البوت هنا
BOT_TOKEN = "38455680-5c03-47ce-9516-6e41560b542e"

# 📢 يوزر القناة
CHAT_ID = "@Gol_lives"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
    
    print(response.text)

print("Bot started at:", datetime.now())

# ✅ رسالة عند التشغيل
send_message(f"✅ Bot started\n⏰ {datetime.now()}")

while True:
    try:
        send_message(f"✅ Bot is alive\n⏰ {datetime.now()}")
        time.sleep(300)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
