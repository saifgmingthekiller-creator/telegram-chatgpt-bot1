import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

BOT_TOKEN = os.getenv("8395211430:AAFXxPNeQXLhMmFveDqUhPavY_mIySqYbUI")
client = OpenAI(api_key=os.getenv("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"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! ابعتلي أي سؤال")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "أنت مساعد ذكي تتكلم عربي"},
            {"role": "user", "content": msg}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
