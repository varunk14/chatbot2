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
        title = top_result.get('title', 'No title available')  # Use default if missing
        snippet = top_result.get('snippet', 'No description available, Harini papa')  # Avoid KeyError
        link = top_result.get('link', '')

        return f"**{title}**\n\n{snippet}\n\nRead more: {link}" if link else f"**{title}**\n\n{snippet}"
    else:
        return "Sorry, I couldn't find any relevant information, Harini papa!"



# Function to get a random compliment from the API
def get_compliment():
    try:
        response = requests.get("https://complimentr.com/api")
        data = response.json()
        return data["compliment"].capitalize()
    except Exception as e:
        return "Good morning, Harini! You are truly amazing! 💖"

# Function to send a morning message with a compliment
def send_morning_message(update: Update, context):
    compliment = get_compliment()
    message = f"Good morning, Harini! ☀️ {compliment}"
    update.message.reply_text(message)



# Function to greet based on the time of day
def get_greeting():
    current_hour = datetime.datetime.now().hour  # Get the current hour
    if 12 <= current_hour < 17:
        return "Good afternoon Harini papa!"
    elif 17 <= current_hour < 21:
        return "Good evening Harini papa!"
    else:
        return "Good night Harini papa!"






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
