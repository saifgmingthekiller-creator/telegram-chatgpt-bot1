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

# ==============================
# إعدادات أساسية
# ==============================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("8395211430:AAFXxPNeQXLhMmFveDqUhPavY_mIySqYbUI")

if not OPENAI_KEY:
    raise ValueError("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")

client = OpenAI(api_key=OPENAI_KEY)

# ==============================
# أوامر البوت
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك!\n\n"
        "أنا بوت ذكاء اصطناعي 🤖\n"
        "اكتب أي سؤال وأنا هجاوبك فورًا."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 الأوامر المتاحة:\n\n"
        "/start - تشغيل البوت\n"
        "/help - عرض المساعدة\n\n"
        "أو ابعت أي رسالة عادية وهرد عليك."
    )

# ==============================
# الرد على الرسائل
# ==============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that speaks Arabic."},
                {"role": "user", "content": user_text}
            ],
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ حصل خطأ أثناء المعالجة، حاول مرة تانية.")

# ==============================
# تشغيل التطبيق
# ==============================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
