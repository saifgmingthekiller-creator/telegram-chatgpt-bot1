import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

# قراءة المتغيرات من Railway
BOT_TOKEN = os.getenv("8395211430:AAFXxPNeQXLhMmFveDqUhPavY_mIySqYbUI")
OPENAI_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_KEY)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تتكلم عربي"},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("حصل خطأ 😢 حاول تاني")
        print(e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
