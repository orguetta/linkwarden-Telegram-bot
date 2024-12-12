import os
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import Conflict, TelegramError, TimedOut, NetworkError
import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
LINKWARDEN_API_URL = os.environ.get('LINKWARDEN_API_URL')
LINKWARDEN_API_KEY = os.environ.get('LINKWARDEN_API_KEY')
LINKWARDEN_COLLECTION_ID = os.environ.get('LINKWARDEN_COLLECTION_ID')

# Configure requests to retry on failure
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
with requests.Session() as http:
    http.mount("https://", adapter)
    http.mount("http://", adapter)

async def start(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, 
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
    }
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = http.post(f'{LINKWARDEN_API_URL}/api/v1/links', json=data, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Successfully added link to Linkwarden: {url}")
            return True
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to add link after {max_retries} attempts: {e}")
                return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return False
        except requests.RequestException as e:
            logger.error(f"Failed to add link to Linkwarden: {e}")
            return False

async def handle_message(update: Update, context: CallbackContext) -> None:
    # Initialize message text
    message = update.message.text

    # Check if the message is forwarded
    if hasattr(update.message, 'forward_from') or hasattr(update.message, 'forward_from_chat'):
        # If it's forwarded, you can still use the same message text
        message = update.message.text

    links = extract_links(message)
    
    if not links:
        await send_message_with_retry(update, context, "No links found in the message.")
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

    await send_message_with_retry(update, context, response)

async def send_message_with_retry(update: Update, context: CallbackContext, text: str, max_retries: int = 3) -> None:
    for attempt in range(max_retries):
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            return
        except TimedOut as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to send message after {max_retries} attempts: {e}")
                raise

async def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if isinstance(context.error, (TimedOut, NetworkError)):
        logger.info("Network error occurred. The message might have been sent despite the error.")
    elif update and update.effective_chat:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                           text="An error occurred. The developer has been notified.")
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    while True:
        try:
            application.run_polling(timeout=10, poll_interval=10)  # Set poll_interval to 10 seconds
        except Conflict:
            logger.error("Conflict error occurred. Waiting before restarting...")
            time.sleep(30)
        except NetworkError as e:
            logger.error(f"Network error occurred: {e}. Restarting...")
            time.sleep(10)
        except TelegramError as e:
            logger.error(f"TelegramError occurred: {e}. Waiting before restarting...")
            time.sleep(30)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}. Exiting...")
            break

if __name__ == '__main__':
    main()
