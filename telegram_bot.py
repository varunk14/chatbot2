import datetime
import requests
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder

# Replace with your actual tokens
TELEGRAM_TOKEN = '7874095227:AAH518vR66DVg6gg3MTVoiCXbUcvActw6t0'
GOOGLE_API_KEY = 'AIzaSyAXtQ4ryCWr5fc-ly_z911uhhzpPAA0c6k'
GOOGLE_CX = 'a4bf1413548474c46'

# Function to fetch concise information from Google Search
def get_google_answer(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
    response = requests.get(search_url)
    data = response.json()

    if 'items' in data:
        top_result = data['items'][0]  # Get the top result
        title = top_result['title']
        snippet = top_result.get('snippet', 'No description available')  # Handling missing snippet
        link = top_result['link']
        return f"**{title}**\n\n{snippet}\n\nRead more: {link}"
    else:
        return "Sorry, I couldn't find any relevant information ,Harini papa!."








# Function to greet based on the time of day
def get_greeting():
    current_time = datetime.datetime.now().hour
    if current_time < 12:
        return "Good morning Harini papa!"
    elif current_time < 18:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"

# Command handler to start the bot and greet
async def start(update: Update, context):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today?")

# Function to respond to questions

async def respond(update: Update, context):
    question = update.message.text
    print(f"User asked: {question}")  # This logs the question in the terminal

    answer = get_google_answer(question)
    print(f"Bot answered: {answer}")  # This logs the answer in the terminal
    log_entry = f"User: {question}\nBot: {answer}\n\n"

    # Save logs to a text file
    with open("chat_log.txt", "a") as log_file:
        log_file.write(log_entry)

    await update.message.reply_text(answer)


# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    app.run_polling()

if __name__ == '__main__':
    main()
