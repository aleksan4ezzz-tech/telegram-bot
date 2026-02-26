from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Ваш токен
TOKEN = "8217980258:AAHed5tCiB1XVRkFb1RgEY2VXg4kOGG_wGg"
# Секретный путь для webhook (можно сгенерировать случайный)
WEBHOOK_PATH = f"/{TOKEN}"

# Создаем Flask приложение
app = Flask(__name__)

# Создаем бота
bot = Bot(token=TOKEN)

# Создаем диспетчер
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Словарь языков
languages = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇩🇪 Deutsch": "de"
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🇷🇺 Русский", "🇬🇧 English", "🇩🇪 Deutsch"]]
    await update.message.reply_text(
        "Выберите язык / Choose language / Sprache wählen",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Текстовые сообщения
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
    else:
        await update.message.reply_text("Я не понимаю эту команду.")

# Регистрируем обработчики
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

# Главный маршрут для Telegram webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Главная страница (можно проверить, что сайт живой)
@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # На Render порт берется из переменной окружения PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)