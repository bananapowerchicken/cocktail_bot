# main start file, where the bot runs

import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router
from app.database.models import async_main


# load vars from .env file 
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


async def main():
    await async_main()

    bot = Bot(token=BOT_TOKEN) # create bot    
    dp = Dispatcher() # create dispatcher
    dp.include_router(router) # connect to handlers with this router   
    await dp.start_polling(bot) # run bot


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # wrap in try except to see nice error instead of KeyboardInterrupt
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')