import datetime
import pytz
import requests
from telegram import Update
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging to see errors clearly
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to log errors
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

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
        snippet = top_result.get('snippet', 'No description available')  # Avoid KeyError
        link = top_result.get('link', '')

        return f"**{title}**\n\n{snippet}\n\nRead more: {link}" if link else f"**{title}**\n\n{snippet}"
    else:
        return "Sorry, I couldn't find any relevant information, Harini papa."


# Function to greet based on the time of day
def get_greeting():
    tz = pytz.timezone("Asia/Kolkata")  # Indian Standard Time (IST)
    current_time = datetime.datetime.now(tz).hour  # Get local hour

    if current_time < 12:
        return "Good morning Harini papa!"
    elif current_time < 17:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"


# Function to fetch music recommendations based on language or mood
def get_music_recommendation(language=None, mood=None):
    base_url = "https://saavn.dev/api/songs?query="  # Unofficial JioSaavn API
    
    # If a language is provided, form the query
    if language:
        query = f"best {language} songs"
    # If mood is provided, form the query based on mood
    elif mood:
        query = f"{mood} mood songs"
    else:
        return "Please specify a language or mood for song recommendations, Harini papa."
    
    # Replace spaces in query with %20 for URL encoding
    api_url = base_url + query.replace(" ", "%20")
    
    # Get data from the API
    response = requests.get(api_url)
    data = response.json()
    
    # Check if there are valid data in response
    if data.get("data"):
        music_list = []
        for song in data["data"][:5]:  # Get top 5 songs
            track_name = song['title']
            artist = song['primaryArtists']
            play_url = song['media_url']
            music_list.append(f"🎵 *{track_name}* - {artist}\n[Play Now]({play_url})\n")
        
        return "\n\n".join(music_list)
    else:
        return f"Sorry, I couldn't find any music recommendations right now for {language or mood}, Harini papa."






        

# Command handler to start the bot and greet
async def start(update: Update, context: CallbackContext):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today?")

# Updated respond function with mood and language handling
async def respond(update: Update, context: CallbackContext):
    question = update.message.text.lower()
    print(f"User asked: {question}")  # This logs the question in the terminal

    if "song" in question or "music" in question:
        language = None
        mood = None

        if "hindi" in question:
            language = "hindi"
        elif "english" in question:
            language = "english"
        elif "telugu" in question:
            language = "telugu"
        elif "tamil" in question:
            language = "tamil"
        
        if "happy" in question:
            mood = "happy"
        elif "sad" in question:
            mood = "sad"
        elif "party" in question:
            mood = "party"
        elif "chill" in question:
            mood = "chill"
        elif "romantic" in question:
            mood = "romantic"
        
        answer = get_music_recommendation(language, mood)
    else:
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
    app.add_error_handler(error_handler)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    app.run_polling()

if __name__ == '__main__':
    main()
