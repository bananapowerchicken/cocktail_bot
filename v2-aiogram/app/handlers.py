# separately stored handlers

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router() # a connecting obj with run file

@router.message(CommandStart())
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Hello, I'm a cocktail bot!") # a handler for start command
