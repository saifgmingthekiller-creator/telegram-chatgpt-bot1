import os
import logging
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# ======================
# Logging
# ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BOT_TOKEN = os.getenv("8395211430:AAFBz6EDESfqJ-4kcUMKR94QsdUDqjqYAbg")
OPENAI_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_KEY)

# ======================
# Commands
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً!\n"
        "اكتب أي سؤال بأي لغة وأنا هرد عليك 🤖"
    )

# ======================
# Message Handler
# ======================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    # علامة إن البوت بيكتب
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Reply in the same language as the user."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            timeout=30
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        await update.message.reply_text(
            "❌ حصل خطأ أثناء الإجابة.\n"
            "جرب سؤال تاني أو بعد شوية."
        )

# ======================
# App
# ======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
