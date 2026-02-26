from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

# ==== Токен и бот ====
TOKEN = "8217980258:AAHed5tCiB1XVRkFb1RgEY2VXg4kOGG_wGg"
bot = Bot(token=TOKEN)

# ==== Flask приложение ====
app = Flask(__name__)

# ==== Синхронный диспетчер ====
dp = Dispatcher(bot, None, workers=0, use_context=True)

# ==== Обработчики команд ====
def start(update: Update, context):
    update.message.reply_text("Привет! Я бот, работающий через Render free webhook.")

def help_command(update: Update, context):
    update.message.reply_text("Напиши что-нибудь, и я повторю это!")

def echo(update: Update, context):
    update.message.reply_text(f"Ты написал: {update.message.text}")

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ==== Webhook для Telegram ====
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)  # синхронная обработка
    return "OK"

# ==== Проверка работы сервиса ====
@app.route("/")
def index():
    return "Bot is running!"

# ==== Запуск сервера ====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)