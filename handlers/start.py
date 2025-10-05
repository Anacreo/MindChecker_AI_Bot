import logging
from aiogram import F, Router
from aiogram.types import Message

router = Router()
@router.message(F.text == "/start")
async def handle_start(message: Message):
    logging.info(f"Received /start from {message.from_user.id}")
    await message.answer("Welcome to MindChecker AI Bot!")
