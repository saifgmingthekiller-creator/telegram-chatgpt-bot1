import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Tokens from Railway Variables
TELEGRAM_TOKEN = os.getenv("8395211430:AAFBz6EDESfqJ-4kcUMKR94QsdUDqjqYAbg")
OPENAI_API_KEY = os.getenv("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")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found!")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found!")

client = OpenAI(api_key=OPENAI_API_KEY)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! ابعتلي أي سؤال وأنا هرد عليك.")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_text},
            ],
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("حصل خطأ 😅 جرب تاني.")
        print(e)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
