from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# ====== Настройки ======
TOKEN = "8217980258:AAHed5tCiB1XVRkFb1RgEY2VXg4kOGG_wGg"

# ====== Flask ======
app = Flask(__name__)

# ====== Telegram Bot ======
telegram_app = ApplicationBuilder().token(TOKEN).build()

# ---- Команда /start ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот работает через Render free webhook.")

telegram_app.add_handler(CommandHandler("start", start))

# ---- Инициализация Telegram приложения ----
asyncio.get_event_loop().create_task(telegram_app.initialize())
asyncio.get_event_loop().create_task(telegram_app.start())

# ====== Webhook ======
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Обрабатываем POST запросы от Telegram"""
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    # Отправляем обновление в очередь обработчиков
    asyncio.get_event_loop().create_task(telegram_app.update_queue.put(update))
    return "OK"

# ====== Проверка работы ======
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# ====== Локальный запуск (опционально) ======
if __name__ == "__main__":
    # Если хочешь тестировать локально с polling
    telegram_app.run_polling()