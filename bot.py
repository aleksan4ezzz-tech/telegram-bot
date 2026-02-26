from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))  # Render сам выдаст порт

bot = Bot(TOKEN)
app = Flask(__name__)
telegram_app = None  # для ApplicationBuilder

languages = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🇷🇺 Русский", "🇬🇧 English", "🇩🇪 Deutsch"]]
    await update.message.reply_text(
        "Выберите язык / Choose language / Sprache wählen",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in languages:
        context.user_data["lang"] = languages[text]

        menu = [
            ["📦 Мои посылки", "➕ Добавить посылку"],
            ["❌ Проблема", "⚙️ Настройки"]
        ]

        await update.message.reply_text(
            "Главное меню:",
            reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
        )

# --- Flask route для Telegram webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Принимаем апдейты от Telegram и отправляем в бот"""
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

async def setup_telegram_app():
    global telegram_app
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    await telegram_app.initialize()  # инициализация без run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup_telegram_app())
    # Запуск Flask на Render
    app.run(host="0.0.0.0", port=PORT)