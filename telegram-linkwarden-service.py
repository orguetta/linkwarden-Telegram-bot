import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import re

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
LINKWARDEN_API_URL = os.environ.get('LINKWARDEN_API_URL')
LINKWARDEN_API_KEY = os.environ.get('LINKWARDEN_API_KEY')
LINKWARDEN_COLLECTION_ID = os.environ.get('LINKWARDEN_COLLECTION_ID')  # New environment variable

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Send me a message with links, and I'll add them to Linkwarden!")

def extract_links(text: str) -> list:
    url_pattern = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_+.~#?&/=]*')
    return url_pattern.findall(text)

def add_to_linkwarden(url: str) -> bool:
    headers = {
        'Authorization': f'Bearer {LINKWARDEN_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'url': url,
        'collectionId': LINKWARDEN_COLLECTION_ID,
        # Add any additional fields required by Linkwarden API
    }
    try:
        response = requests.post(f'{LINKWARDEN_API_URL}/api/v1/links', json=data, headers=headers)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to add link to Linkwarden: {e}")
        return False

def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    links = extract_links(message)
    
    if not links:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="No links found in the message.")
        return

    successful_links = []
    failed_links = []

    for link in links:
        if add_to_linkwarden(link):
            successful_links.append(link)
        else:
            failed_links.append(link)

    response = "Links added to Linkwarden:\n" + "\n".join(successful_links)
    if failed_links:
        response += "\n\nFailed to add these links:\n" + "\n".join(failed_links)

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()