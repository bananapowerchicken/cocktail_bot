from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os
import logging


# load vars from .env file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# global dictionary with states of different chat_ids
user_state = {}

# list of ingredients, that user has and prints in bot
ingredients = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an introduction to a new user"""

    # add menu
    # buttons
    keyboard = [
        ["Wanna cocktail🍹", "Stop"],
        ["Help - mock"] # mock now
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # welcome-text + menu(keyboard)
    await update.message.reply_text(
        'Welcome to the Cocktail Bot! Choose an option and press the button', 
        reply_markup=reply_markup
    )

async def collect_ingredients(update, context) -> None:
    """Collect ingredients form the user message if 'waiting_for_ingredients' state is active."""
    chat_id = update.effective_chat.id
    
    if user_state.get(chat_id) == 'waiting_for_ingredients':
        ingredients.append(update.message.text)
        await update.message.reply_text(f"Added: {update.message.text}") # to check

async def wanna_cocktail(update, context) -> None:
    """Resend you formatted ingredients with additional text"""
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Wanna cocktail? Gimme ingredients")

    # Set user state for this chat_id to 'waiting_for_ingredients'
    user_state[chat_id] = 'waiting_for_ingredients'

async def stop_waiting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop waiting for ingredients and reset user state."""
    chat_id = update.effective_chat.id
    
    # Reset user state
    user_state.pop(chat_id, None)
    
    # Optionally send a message confirming the state has been reset
    await context.bot.send_message(chat_id=chat_id, text="Stopped waiting for ingredients.")

    ingredients_list = ''
    if ingredients != '':
        for i in ingredients:
            ingredients_list+=f'{i} \n'


    await context.bot.send_message(chat_id=chat_id, text=f"So you wanna cocktail from:\n {ingredients_list}")

def main():
    "Main bot logic"
    # connect my bot to this code by token (API)
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # menu button handler
    # Regex must fully match!!!
    wanna_handler = MessageHandler(filters.TEXT & filters.Regex('^Wanna cocktail🍹$'), wanna_cocktail)
    application.add_handler(wanna_handler)

    collect_handler = MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex('^Stop$'), collect_ingredients)
    application.add_handler(collect_handler)

    stop_handler = MessageHandler(filters.TEXT & filters.Regex('^Stop$'), stop_waiting)
    application.add_handler(stop_handler)

    # start working until ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()