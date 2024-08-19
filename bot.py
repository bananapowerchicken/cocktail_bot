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
ingredients = {}

# TEST
# tmp db
# TO DO: move to real DB - not llocal dict
db_cocktails = {
    'Whiskey-Cola': {
        'ingredients': ['whiskey', 'cola'],
        'recipe': 'mix it!'
    },
    'Whiskey-Cola-Lemon': {
        'ingredients': ['whiskey', 'cola', 'lemon'],
        'recipe': 'mix it and add lemon!'
    },
    'Gin-Tonic': {
        'ingredients': ['gin', 'tonic'],
        'recipe': 'splish - splash and ready'
    },
    'Electric lemonade': {
        'ingredients': ['vodka', 'lemon juice', 'sugar syrup', 'lemonade', 'blue curacao liqueur'],
        'recipe': 'vodka 45 ml + lemon juice 30 ml + sugar syrup 15 ml + lemonade 60 ml + blue curacao liqueur 10 ml. Shake and enjoy! '
    },

    
}

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
        ingredient = update.message.text.lower()
        if chat_id not in ingredients:
            ingredients[chat_id] = []
        ingredients[chat_id].append(ingredient)
        await update.message.reply_text(f"Added: {ingredient}")

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

    # Find matching cocktails
    matching_cocktails = []
    user_ingreds = set(ingredients.get(chat_id, []))
    
    for cocktail, details in db_cocktails.items():
        if user_ingreds.issuperset(details["ingredients"]):
            matching_cocktails.append(cocktail)
    
    if matching_cocktails:
        cocktail_list = ''
        for cocktail in matching_cocktails:
            cocktail_list += f"{cocktail}\n{db_cocktails[cocktail]['recipe']}\n\n"
        await context.bot.send_message(chat_id=chat_id, text=f"Based on your ingredients, you can make:\n{cocktail_list}")
    else:
        await context.bot.send_message(chat_id=chat_id, text="No cocktails found with those ingredients.")
    
    # Clear ingredients list for this user
    ingredients.pop(chat_id, None)

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