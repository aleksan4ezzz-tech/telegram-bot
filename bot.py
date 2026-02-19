from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

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

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot running...")
    app.run_polling()  # <-- запускаем без await и asyncio.run

if __name__ == "__main__":
    main()
