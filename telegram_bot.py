import os
import requests
import datetime
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Initialize Flask for Railway
app = Flask(__name__)

# Telegram Bot Token (Set this in Railway environment variables)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize Telegram Bot Application
app_telegram = Application.builder().token(TOKEN).build()

# Function to get correct greeting based on time
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning, Harini papa! 🌞"
    elif 12 <= hour < 18:
        return "Good afternoon, Harini papa! ☀️"
    else:
        return "Good evening, Harini papa! 🌙"

# Function to get an answer from Google (or use another API)
def get_google_answer(question):
    search_url = "https://api.duckduckgo.com/?q=" + question + "&format=json"
    response = requests.get(search_url).json()
    
    if "AbstractText" in response and response["AbstractText"]:
        return response["AbstractText"]
    return "Sorry Harini, I couldn't find an answer for that."

# Function to get music recommendations based on language
def get_music_recommendation(language):
    api_url = f"https://api.deezer.com/search?q={language}&limit=5"
    response = requests.get(api_url).json()

    if 'data' in response:
        music_list = []
        for track in response['data']:
            track_name = track['title']
            artist = track['artist']['name']
            music_list.append(f"🎵 {track_name} - {artist}")
        return "\n".join(music_list)
    else:
        return "Sorry, Harini, I couldn't find any songs right now."

# Command handler for /start
async def start(update: Update, context):
    await update.message.reply_text(get_greeting() + "\nHow can I help you today?")

# Respond to messages
async def respond(update: Update, context):
    question = update.message.text
    answer = get_google_answer(question)
    await update.message.reply_text(answer)

# Music recommendation command
async def recommend_music(update: Update, context):
    language = "english"  # Default to English
    if context.args:
        language = context.args[0].lower()
    
    recommendations = get_music_recommendation(language)
    await update.message.reply_text(recommendations)

# Error handling
async def error(update: Update, context):
    print(f"Error: {context.error}")

# Add Telegram Handlers
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("music", recommend_music))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
app_telegram.add_error_handler(error)

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), app_telegram.bot)
    app_telegram.process_update(update)
    return "OK", 200

# Set Telegram Webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    WEBHOOK_URL = "https://your-railway-app.up.railway.app/webhook"
    app_telegram.bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}", 200

# Railway keeps the app alive
@app.route('/')
def home():
    return "Telegram Bot is running on Railway!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
