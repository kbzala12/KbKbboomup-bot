bot_combined.py
import telebot, sqlite3, os
from flask import Flask
from threading import Thread

# ========== CONFIG ==========
BOT_TOKEN = "8267991203:AAENDUbZ9tsyCeOWFVvPUzl--n9nqaUBRts"
ADMIN_ID = @Kbzala12
YOUTUBE_CHANNEL = "https://youtube.com/@kishorsinhzala.?si=uKMVwnB7wV_yoSQN"
TELEGRAM_GROUP = "https://telegram.me/boomupbot10"
# ========== KEEP ALIVE (for Replit) ==========
app = Flask('')
@app.route('/')
def home(): return "Bot is running"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()
keep_alive()

# ========== DB SETUP ==========
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    points INTEGER DEFAULT 0,
    videos INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    ref INTEGER DEFAULT 0,
    referred_by TEXT
)
""")
conn.commit()
# ========== DB FUNCTIONS ==========
def check_user(user_id):
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
        conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return {"id": row[0], "points": row[1], "videos": row[2], "shares": row[3], "ref": row[4], "referred_by": row[5]} if row else None

def add_points(user_id, field, max_limit, increment, points):
    cursor.execute(f"SELECT {field}, points FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0] < max_limit:
        cursor.execute(f"UPDATE users SET {field} = {field} + ?, points = points + ? WHERE id = ?", (increment, points, user_id))
        conn.commit()
        return True
    return False

def apply_referral(new_user_id, ref_id):
    if new_user_id == ref_id: return
    user = get_user(new_user_id)
    if user["referred_by"]: return
    if get_user(ref_id):
        cursor.execute("UPDATE users SET ref = ref + 1, points = points + 50 WHERE id = ?", (ref_id,))
        cursor.execute("UPDATE users SET referred_by = ? WHERE id = ?", (ref_id, new_user_id))
        conn.commit()

def get_top_users(limit=10):
    cursor.execute("SELECT id, points FROM users ORDER BY points DESC LIMIT ?", (limit,))
    return cursor.fetchall()