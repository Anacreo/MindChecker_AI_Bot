import logging
from aiogram import F, Router
from aiogram.types import Message

router = Router()
@router.message(F.text == "/start")
async def handle_start(message: Message):
    user = message.from_user
    logging.info(
        f"Received /start from user_id={user.id}, username={user.username}, "
        f"first_name={user.first_name}, last_name={user.last_name}, language_code={user.language_code}"
    )

    await message.answer(
        "👋 Welcome to MindChecker AI Bot!\n\n"
        "Here’s what I can help you with:\n"
        "• 🧠 Mental health check-in (/phq9)\n"
        "• 📊 View your progress (coming soon)\n"
        "• ⚙️ Settings and preferences (coming soon)\n\n"
        "Just type a command or tap a button to begin!"
    )
