# separately stored handlers

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.keyboards as kb

router = Router() # a connecting obj with run file

@router.message(CommandStart())
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Hello, I'm a cocktail bot!", reply_markup=kb.main_kb) # a handler for start command


@router.message(lambda message: message.text == 'Gimme cocktails!')
async def command_give_instruction_handler(message: Message):
    """
    This handler sends an instruction after pressing Gimme cocktail btn
    """
    await message.answer('Please, type your ingredients')