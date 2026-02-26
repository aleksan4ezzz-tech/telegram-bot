from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import asyncio

TOKEN = os.environ.get("8217980258:AAHed5tCiB1XVRkFb1RgEY2VXg4kOGG_wGg")
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

languages = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает 🚀")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сообщение получено")

telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    asyncio.run(telegram_app.initialize())
    asyncio.run(telegram_app.start())
    app.run(host="0.0.0.0", port=PORT)