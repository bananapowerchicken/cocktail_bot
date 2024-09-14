# main start file, where the bot runs

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher


async def main():    
    bot = Bot(token='') # create bot    
    dp = Dispatcher(bot) # create dispatcher
    await dp.start_polling() # run bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # wrap in try except to see nice error instead of KeyboardInterrupt
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')