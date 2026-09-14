import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import groq
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = groq.Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam dayı! Ben DayıBot. Bana ne sormak istersin?")

async def cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mesaji = update.message.text
    await update.message.reply_chat_action("typing")
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": user_mesaji}],
            model="llama3-8b-8192",
        )
        cevap = chat_completion.choices[0].message.content
        await update.message.reply_text(cevap)
    except Exception as e:
        await update.message.reply_text(f"Dayı bi hata oldu: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cevapla))
    print("Bot çalışıyor...")
    app.run_polling()
