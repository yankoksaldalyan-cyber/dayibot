import os
import telebot
from groq import Groq

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Ben DayıBot 🤖 Groq AI ile çalışıyorum. Bana bir şey sor!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": message.text}],
            model="llama3-8b-8192",
        )
        cevap = chat_completion.choices[0].message.content
        bot.reply_to(message, cevap)
    except Exception as e:
        bot.reply_to(message, f"Bir hata oldu: {e}")

print("Bot çalışıyor...")
bot.polling()
