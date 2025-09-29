from aiogram import F, Router
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Hi! I'm MindChecker. Ready to help you reflect and assess your mental health.")
