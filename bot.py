from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os


# load vars from .env file
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')



# add 1st functionality - hello-message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Sends an introduction to a new user"
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I am a cocktail bot!")

# trial get ingredients handler
async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Sends an introduction to a new user"
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Gimme ingredients!!!")

def main():
    "Main bot logic"
    # connect my bot to this code by token (API)
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # trial get handler
    get_handler = CommandHandler('get', get)
    application.add_handler(get_handler)

    # start working until ctrl+C
    application.run_polling()

if __name__ == '__main__':
    main()