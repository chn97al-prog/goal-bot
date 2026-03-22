import requests
import time
from datetime import datetime

# 🔑 ضع توكن البوت هنا
BOT_TOKEN = "8349173390:AAHPUyO54QOpC0mZKhrwKlC6krsP31TpzNg"

# 📢 يوزر القناة
CHAT_ID = "@Gol_lives"

# 📤 دالة الإرسال مع طباعة الأخطاء
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        })

        # طباعة الرد الكامل للتشخيص
        print("Response:", response.text)

        # تحقق من نجاح الإرسال
        data = response.json()
        if not data.get("ok"):
            print("❌ Error:", data.get("description"))

    except Exception as e:
        print("Exception:", e)

# 🚀 تشغيل البوت
print("Bot started at:", datetime.now())

# ✅ رسالة اختبار عند التشغيل
send_message(f"✅ Bot started successfully\n⏰ {datetime.now()}")

# 🔁 تشغيل مستمر
while True:
    try:
        # رسالة تحقق
        send_message(f"✅ Bot is alive\n⏰ {datetime.now()}")

        time.sleep(300)

    except Exception as e:
        print("Loop error:", e)
        time.sleep(5)
