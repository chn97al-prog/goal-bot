import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔐 قراءة المتغيرات من Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🎛️ أزرار
keyboard = [
    ["🎨 Generate Image", "🖼️ Edit Image"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 أهلاً بك في بوت الصور\nاختر من الأزرار 👇",
        reply_markup=markup
    )


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
        "prompt": prompt,
        "size": "1024x1024"
    }

    res = requests.post(url, headers=headers, files=files, data=data)
    return res.json()["data"][0]["url"]


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    # 🎨 اختيار إنشاء صورة
    if text == "🎨 Generate Image":
        context.user_data["mode"] = "generate"
        update.message.reply_text("✍️ اكتب وصف الصورة")

    # 🖼️ اختيار تعديل صورة
    elif text == "🖼️ Edit Image":
        context.user_data["mode"] = "edit"
        update.message.reply_text("📷 أرسل الصورة مع وصف في الكابشن")

    # 📷 إذا المستخدم أرسل صورة
    elif update.message.photo:
        file = update.message.photo[-1].get_file()
        file_path = "input.jpg"
        file.download(file_path)

        prompt = update.message.caption or "Edit this image"

        update.message.reply_text("⏳ جاري تعديل الصورة...")

        try:
            img_url = edit_image(file_path, prompt)
            update.message.reply_photo(photo=img_url)
        except:
            update.message.reply_text("❌ فشل تعديل الصورة")

    else:
        # 🎨 نص → إنشاء صورة
        prompt = text

        update.message.reply_text("⏳ جاري إنشاء الصورة...")

        try:
            img_url = generate_image(prompt)
            update.message.reply_photo(photo=img_url)
        except:
            update.message.reply_text("❌ فشل إنشاء الصورة")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.all, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
