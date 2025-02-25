import datetime
import os
import pytz
import requests
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in Railway env

# Flask app for webhook
app = Flask(__name__)

# Function to get AI response
def get_ai_response(query):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": "You are a helpful AI assistant."},
                     {"role": "user", "content": query}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    
    # Log API response
    logging.info(f"API Response: {response.text}")

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"] if "choices" in data else "Sorry, I couldn't fetch a response. Please try again."
    except Exception as e:
        logging.error(f"Error parsing API response: {e}")
        return "Sorry, I couldn't fetch a response. Please try again."

# Function to get greeting
def get_greeting():
    tz = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.datetime.now(tz).hour

    if current_hour < 12:
        return "Good morning Harini papa!"
    elif current_hour < 17:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"

# Telegram handlers
async def start(update: Update, context: CallbackContext):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today?")

async def respond(update: Update, context: CallbackContext):
    question = update.message.text
    answer = get_ai_response(question)

    # Log user queries
    logging.info(f"User: {question}")
    logging.info(f"Bot: {answer}")

    await update.message.reply_text(answer)

# Telegram bot setup
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# Webhook route for Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), telegram_app.bot)
    asyncio.create_task(telegram_app.process_update(update))  # Use async task
    return "OK", 200

# Set Telegram Webhook
async def set_telegram_webhook():
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    logging.info(f"Webhook set at: {WEBHOOK_URL}/webhook")

# Start Flask app
if __name__ == "__main__":
    # Run the async webhook setup in an event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_telegram_webhook())

    # Run Flask
    app.run(host="0.0.0.0", port=8000)
