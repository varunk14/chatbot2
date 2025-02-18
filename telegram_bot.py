import datetime
import pytz
import requests
from telegram import Update
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with actual API keys
TELEGRAM_TOKEN = '7874095227:AAH518vR66DVg6gg3MTVoiCXbUcvActw6t0'
OPENROUTER_API_KEY = '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'  # Replace with a real OpenRouter API key
GOOGLE_API_KEY = 'AIzaSyAXtQ4ryCWr5fc-ly_z911uhhzpPAA0c6k'  # Replace with your Google Search API key
GOOGLE_CX = 'a4bf1413548474c46'  # Replace with your Google Custom Search Engine ID

# ✅ Function to log errors
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

# ✅ Function to fetch AI-generated response using OpenRouter (FREE AI API)
def get_ai_response(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "messages": [{"role": "system", "content": "You are a helpful AI assistant."},
                     {"role": "user", "content": query}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    return data['choices'][0]['message']['content'] if "choices" in data else "Sorry, I couldn't fetch a response."

# ✅ Function to fetch concise information from Google Search
def get_google_answer(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
    response = requests.get(search_url)
    data = response.json()

    if 'items' in data:
        top_result = data['items'][0]
        title = top_result.get('title', 'No title available')
        snippet = top_result.get('snippet', 'No description available')
        link = top_result.get('link', '')

        return f"**{title}**\n\n{snippet}\n\nRead more: {link}" if link else f"**{title}**\n\n{snippet}"
    else:
        return "Sorry, I couldn't find any relevant information, Harini papa."

# ✅ Function to greet based on time
def get_greeting():
    tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.datetime.now(tz).hour

    if current_time < 12:
        return "Good morning Harini papa!"
    elif current_time < 17:
        return "Good afternoon Harini papa!"
    else:
        return "Good evening Harini papa!"

# ✅ Function to fetch music recommendations (FIXED API)
def get_music_recommendation(language=None, mood=None):
    base_url = "https://saavn.dev/api/songs?query="  # Replace with a working music API
    
    if language:
        query = f"best {language} songs"
    elif mood:
        query = f"{mood} mood songs"
    else:
        return "Please specify a language or mood for song recommendations, Harini papa."

    api_url = base_url + query.replace(" ", "%20")
    
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return "Sorry, I couldn't fetch music recommendations at the moment."

    data = response.json()
    
    if "data" in data and data["data"]:
        music_list = []
        for song in data["data"][:5]:
            track_name = song['title']
            artist = song['primaryArtists']
            play_url = song.get('media_url', 'No link available')
            music_list.append(f"🎵 *{track_name}* - {artist}\n[Play Now]({play_url})\n")

        return "\n\n".join(music_list)
    else:
        return f"Sorry, I couldn't find any music recommendations for {language or mood}, Harini papa."

# ✅ Command to start the bot
async def start(update: Update, context: CallbackContext):
    greeting = get_greeting()
    await update.message.reply_text(f"{greeting} How can I assist you today?")

# ✅ Main response function (handles AI, music, and Google Search)
async def respond(update: Update, context: CallbackContext):
    question = update.message.text.lower()
    print(f"User asked: {question}")  

    if "song" in question or "music" in question:
        language, mood = None, None

        if any(lang in question for lang in ["hindi", "english", "telugu", "tamil"]):
            language = next(lang for lang in ["hindi", "english", "telugu", "tamil"] if lang in question)

        if any(m in question for m in ["happy", "sad", "party", "chill", "romantic"]):
            mood = next(m for m in ["happy", "sad", "party", "chill", "romantic"] if m in question)

        answer = get_music_recommendation(language, mood)

    else:
        answer = get_google_answer(question)  

    print(f"Bot answered: {answer}")  
    log_entry = f"User: {question}\nBot: {answer}\n\n"

    with open("chat_log.txt", "a") as log_file:
        log_file.write(log_entry)

    await update.message.reply_text(answer, parse_mode="Markdown")

# ✅ Main function to start the bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_error_handler(error_handler)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    app.run_polling()

if __name__ == '__main__':
    main()
