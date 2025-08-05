from flask import Flask, render_template, request, jsonify import sqlite3 import time

app = Flask(name)

DATABASE = 'profile.db'

Util function to get user coins

def get_user(user_id): conn = sqlite3.connect(DATABASE) cursor = conn.cursor() cursor.execute("SELECT coins FROM user_profiles WHERE user_id = ?", (user_id,)) row = cursor.fetchone() conn.close() return row[0] if row else None

Add coins to user

def add_coins(user_id, coins): conn = sqlite3.connect(DATABASE) cursor = conn.cursor() cursor.execute("UPDATE user_profiles SET coins = coins + ? WHERE user_id = ?", (coins, user_id)) conn.commit() conn.close()

@app.route('/') def index(): return render_template('index.html')

@app.route('/watch', methods=['POST']) def watch_video(): user_id = request.form.get('user_id') if not user_id: return jsonify({'status': 'fail', 'message': 'Missing user ID'})

# Simulate 3-minute watch
time.sleep(5)  # Production: replace with JS-based timer in frontend

# Reward
add_coins(user_id, 30)
return jsonify({'status': 'success', 'message': '30 coins added'})

@app.route('/balance', methods=['GET']) def get_balance(): user_id = request.args.get('user_id') if not user_id: return jsonify({'status': 'fail', 'message': 'Missing user ID'})

coins = get_user(user_id)

