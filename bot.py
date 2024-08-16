from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os


# load vars from .env file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

user_state = {}

# add 1st functionality - hello-message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an introduction to a new user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am a cocktail bot!")

# echo func
async def echo(update, context) -> None:
    # """Sends back the text"""
    # user_message = update.message.text
    # await update.message.reply_text(user_message)
    """Echo the user message if they are in 'waiting_for_ingredients' state."""
    chat_id = update.effective_chat.id
    
    if user_state.get(chat_id) == 'waiting_for_ingredients':
        # Echo the message if the user is in 'waiting_for_ingredients' state
        await context.bot.send_message(chat_id=chat_id, text=update.message.text)

# trial custom handler
async def wanna_cocktail(update, context) -> None:
    """Resend you formatted ingredients with additional text"""
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Wanna cocktail? Gimme ingredients")

    # Set user state to 'waiting_for_ingredients'
    user_state[chat_id] = 'waiting_for_ingredients'

async def stop_waiting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop waiting for ingredients and reset user state."""
    chat_id = update.effective_chat.id
    
    # Reset user state
    user_state.pop(chat_id, None)
    
    # Optionally send a message confirming the state has been reset
    await context.bot.send_message(chat_id=chat_id, text="Stopped waiting for ingredients.")

def main():
    "Main bot logic"
    # connect my bot to this code by token (API)
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Создаем обработчик сообщений, который будет вызывать функцию echo при получении любого текста
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)

    # triall wanna_cocktail handler
    wanna_handler = CommandHandler('wanna', wanna_cocktail)
    application.add_handler(wanna_handler)

    stop_handler = CommandHandler('stop', stop_waiting)
    application.add_handler(stop_handler)

    # start working until ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()