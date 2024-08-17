from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os


# load vars from .env file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# global dictionary with states of different chat_ids
user_state = {}

# list of ingredients, that user has and prints in bot
ingredients = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an introduction to a new user"""

    # Создаем кнопку    
    keyboard = [
        [InlineKeyboardButton("Wanna cocktail", callback_data='wanna_cocktail')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am a cocktail bot!")
    await update.message.reply_text('Welcome to the Cocktail Bot! Click the button below to get started.', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    # Определяем, какая кнопка была нажата
    if query.data == 'wanna_cocktail':
        # Выполняем логику, которая была бы в обработчике команды /wanna
        await context.bot.send_message(chat_id=query.message.chat_id, text="Wanna cocktail? Gimme ingredients")


async def collect_ingredients(update) -> None:
    """Collect ingredients form the user message if 'waiting_for_ingredients' state is active."""
    chat_id = update.effective_chat.id
    
    if user_state.get(chat_id) == 'waiting_for_ingredients':
        ingredients.append(update.message.text)

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

    # # Создаем обработчик сообщений, который будет вызывать функцию echo при получении любого текста
    # echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    # application.add_handler(echo_handler)

    # Callback handler for buttons
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)

    # trial wanna_cocktail handler
    wanna_handler = CommandHandler('wanna', wanna_cocktail)
    application.add_handler(wanna_handler)

    stop_handler = CommandHandler('stop', stop_waiting)
    application.add_handler(stop_handler)

    # start working until ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()