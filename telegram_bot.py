import datetime
import pytz
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


# Function to greet based on the time of day

  # Import the pytz library

# Function to get a time-based greeting
def get_greeting():
    # Set timezone (change "Asia/Kolkata" if needed)
    tz = pytz.timezone("Asia/Kolkata")  # Indian Standard Time (IST)
    current_time = datetime.datetime.now(tz).hour  # Get local hour

    if current_time < 12:
        return "Good morning Harini papa!"
    elif current_time < 17:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"







# Function to fetch music recommendations based on language
def get_music_recommendation(language):
    # Deezer API URL to get tracks based on genre/language
    api_url = f"https://api.deezer.com/search?q={language}&limit=5"  # Modify to filter by language
    
    # Get data from Deezer API
    response = requests.get(api_url)
    data = response.json()

    # Fetch top tracks
    if 'data' in data:
        music_list = []
        for track in data['data']:
            track_name = track['title']
            artist = track['artist']['name']
            album = track['album']['title']
            music_list.append(f"Song: {track_name}\nArtist: {artist}\nAlbum: {album}\n")
        return "\n\n".join(music_list)
    else:
        return "Sorry, I couldn't find any music recommendations right now Harini papa."

        
    # Function to handle music recommendation requests
def recommend_music(update: Update, context):
    # Fetch language preference from the user or set it to default
    language = update.message.text.split(" ")[1] if len(update.message.text.split(" ")) > 1 else "english"
    
    # Get music recommendations
    recommendations = get_music_recommendation(language)
    update.message.reply_text(recommendations)
    


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
