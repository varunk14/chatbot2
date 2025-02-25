import datetime
import requests
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
import os
import pytz  # Import for handling time zones

# Get environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

# Set timezone to India (IST)
india_tz = pytz.timezone("Asia/Kolkata")

# Function to fetch concise information from Google Search
def get_google_answer(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
    response = requests.get(search_url)
    data = response.json()

    if 'items' in data:
        top_result = data['items'][0]  # Get the top result
        title = top_result['title']
        snippet = top_result['snippet']  # Concise snippet from the result
        link = top_result['link']
        return f"**{title}**\n\n{snippet}\n\nRead more: {link}"
    else:
        return "Sorry, I couldn't find any relevant information, Harini papa!!!."

# Function to greet based on the **correct** time zone
def get_greeting():
    now = datetime.datetime.now(india_tz)  # Use IST time
    hour = now.hour

    if 5 <= hour < 12:
        return "Good morning Harini papa! ☀️"
    elif 12 <= hour < 17:
        return "Good afternoon Harini papa! 🌞"
    elif 17 <= hour < 21:
        return "Good evening Harini papa! 🌆"
    else:
        return "Good night Harini papa! 🌙"

# Command handler to start the bot and greet
async def start(update: Update, context):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today? 😊")

# Function to respond to user queries
async def respond(update: Update, context):
    question = update.message.text
    answer = get_google_answer(question)
    await update.message.reply_text(answer)

# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
