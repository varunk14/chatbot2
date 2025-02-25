import datetime
import requests
import os
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

# Webhook URL for deployment (update this with your actual Railway domain)
WEBHOOK_URL = "https://chatbot2-production-5e50.up.railway.app/webhook"

# Function to fetch concise information from Google Search
def get_google_answer(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
    response = requests.get(search_url)
    data = response.json()

    if 'items' in data:
        top_result = data['items'][0]  
        title = top_result['title']
        snippet = top_result['snippet']
        link = top_result['link']
        return f"**{title}**\n\n{snippet}\n\nRead more: {link}"
    else:
        return "Sorry, I couldn't find any relevant information, Harini papa!!!."

# Function to greet based on the time of day
def get_greeting():
    current_time = datetime.datetime.now().hour
    if current_time < 12:
        return "Good morning Harini papa!"
    elif current_time < 18:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"

# Command handler to start the bot
async def start(update: Update, context):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today, Harini papa?")

# Function to respond to messages
async def respond(update: Update, context):
    question = update.message.text
    answer = get_google_answer(question)
    await update.message.reply_text(answer)

# Webhook update handler
async def webhook_update(update: Update, context):
    await application.update_queue.put(update)

# Main function
def main():
    global application  # Define application globally
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    print("Bot is running with Webhook...")

    # Run webhook instead of polling
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
