import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import datetime
import requests

# 🔐 Config
BOT_TOKEN = "7559801414:AAG6nHs9zoF9CLDknI9E3c5zBqz8ekcgPXQ"
ADMIN_ID = 7470248597
WEBAPP_URL = "https://kbkbboomup-bot-1.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)

# 📁 Database Init
conn = sqlite3.connect("bot.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0, referred_by INTEGER, last_claim TEXT)""")
conn.commit()

# 🚀 Start Command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (user_id, points) VALUES (?, ?)", (user_id, 0))
        conn.commit()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎁 शुरू करें", web_app={"url": WEBAPP_URL}))
    bot.send_message(message.chat.id, f"नमस्ते {message.from_user.first_name}!\n🎉 वॉच वीडियो और कमाओ रिवॉर्ड पॉइंट्स!\n👇 नीचे क्लिक करें:", reply_markup=markup)

# 📊 Balance Check
@bot.message_handler(commands=["balance"])
def balance(message):
    user_id = message.from_user.id
    c.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result:
        bot.reply_to(message, f"🪙 आपके पास {result[0]} पॉइंट्स हैं।")
    else:
        bot.reply_to(message, "⚠️ पहले /start दबाएं।")

# 👤 Admin Panel
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        total_users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        bot.send_message(message.chat.id, f"👑 एडमिन पैनल\n👥 कुल यूज़र्स: {total_users}")
    else:
        bot.send_message(message.chat.id, "❌ आप एडमिन नहीं हैं।")

# 🧑‍🤝‍🧑 Referral System
@bot.message_handler(commands=['refer'])
def refer(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f"🔗 अपने दोस्तों को इनवाइट करें और बोनस पाएं:\n👇 लिंक शेयर करें:\nhttps://t.me/Hkzyt_bot?start={user_id}")

# 🔄 Callback handler for WebApp data (optional future integration)
@bot.message_handler(content_types=["web_app_data"])
def webapp_data(message):
    bot.send_message(message.chat.id, f"📩 Data received from WebApp:\n{message.web_app_data.data}")

# 🛡 Run Bot
print("🤖 Bot is running...")
bot.infinity_polling()