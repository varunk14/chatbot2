import datetime
import os
import pytz
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
<<<<<<< HEAD
=======

>>>>>>> e0bb80381a772774e25313efe971a387b0c7d144
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenRouter API Key (Replace with your real key)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

<<<<<<< HEAD
=======


# OpenRouter API Key (Replace with your real key)

>>>>>>> e0bb80381a772774e25313efe971a387b0c7d144

# Function to generate AI responses using OpenRouter
def get_ai_response(query):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
<<<<<<< HEAD
        "Authorization": f"sk-or-{OPENROUTER_API_KEY}"

          # Ensure API key is correct
=======

        "Authorization": f"sk-or-{OPENROUTER_API_KEY}",

          # Ensure API key is correct

        
>>>>>>> e0bb80381a772774e25313efe971a387b0c7d144
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral",  # Try changing to "gpt-3.5-turbo" if needed
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    
    # Log the full API response
    logging.info(f"API Response: {response.text}")

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"] if "choices" in data else "Sorry, I couldn't fetch a response. Please try again."
    except Exception as e:
        logging.error(f"Error parsing API response: {e}")
        return "Sorry, I couldn't fetch a response. Please try again."



# Function to get greeting based on time
def get_greeting():
    tz = pytz.timezone("Asia/Kolkata")
    current_hour = datetime.datetime.now(tz).hour

    if current_hour < 12:
        return "Good morning Harini papa!"
    elif current_hour < 17:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"

# Command handler for /start
async def start(update: Update, context: CallbackContext):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today?")



async def respond(update: Update, context: CallbackContext):
    question = update.message.text
    answer = get_ai_response(question)  # Get AI response

    # Log user query and bot response
    logging.info(f"User: {question}")
    logging.info(f"Bot: {answer}")

    await update.message.reply_text(answer)


# Function to handle user messages and reply with AI response
async def respond(update: Update, context: CallbackContext):
    question = update.message.text
    answer = get_ai_response(question)
    await update.message.reply_text(answer)

# Main function to run the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Command Handler
    app.add_handler(CommandHandler("start", start))
    
    # Message Handler (for all text messages)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Run bot
    app.run_polling()

if __name__ == '__main__':
    main()
