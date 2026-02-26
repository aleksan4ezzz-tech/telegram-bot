from flask import Flask, request
import telegram

TOKEN = "8217980258:AAHed5tCiB1XVRkFb1RgEY2VXg4kOGG_wGg"
WEBHOOK_PATH = f"/{TOKEN}"
URL = "https://telegram-bot-1python-bot-py-jhri.onrender.com"  # твой Render URL

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Простая команда /start
def handle_message(update):
    text = update.message.text
    chat_id = update.message.chat.id
    if text == "/start":
        bot.send_message(chat_id, "Привет! Я бот.")
    else:
        bot.send_message(chat_id, f"Вы написали: {text}")

# Webhook маршрут
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    handle_message(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    bot.set_webhook(url=f"{URL}/{TOKEN}")  # устанавливаем webhook
    app.run(host="0.0.0.0", port=port)