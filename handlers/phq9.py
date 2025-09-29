import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

# PHQ-9 questions
questions = [
    "1. Little interest or pleasure in doing things?",
    "2. Feeling down, depressed, or hopeless?",
    "3. Trouble falling or staying asleep, or sleeping too much?",
    "4. Feeling tired or having little energy?",
    "5. Poor appetite or overeating?",
    "6. Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    "7. Trouble concentrating on things, such as reading or watching TV?",
    "8. Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you’ve been moving around a lot more than usual?",
    "9. Thoughts that you would be better off dead or of hurting yourself in some way?"
]

# In-memory session store (can be replaced with Redis or DB)
user_sessions = {}

@router.message(F.text == "/phq9")
async def phq9_start(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_sessions[user_id] = {"index": 0, "answers": []}
    logging.info(f"🧠 PHQ-9 started by user {user_id}")
    await message.answer("🧠 Let's begin the PHQ-9 questionnaire.")
    await send_next_question(message)

@router.message(F.text.in_(["0", "1", "2", "3"]))
async def phq9_response(message: Message):
    user_id = str(message.from_user.id)
    session = user_sessions.get(user_id)

    if not session:
        logging.warning(f"⚠️ Response received from user {user_id} without active session")
        await message.answer("Please start the PHQ-9 questionnaire with /phq9.")
        return

    try:
        score = int(message.text)
    except ValueError:
        logging.warning(f"❌ Invalid input from user {user_id}: {message.text}")
        await message.answer("Please respond with a number between 0 and 3.")
        return

    session["answers"].append(score)
    session["index"] += 1
    logging.info(f"📥 User {user_id} answered Q{session['index']}: {score}")

    if session["index"] < len(questions):
        await send_next_question(message)
    else:
        total_score = sum(session["answers"])
        logging.info(f"✅ PHQ-9 complete for user {user_id}. Total score: {total_score}")
        await message.answer(f"✅ PHQ-9 complete. Your total score is: {total_score}")
        del user_sessions[user_id]

async def send_next_question(message: Message):
    user_id = str(message.from_user.id)
    session = user_sessions.get(user_id)

    if session and session["index"] < len(questions):
        question = questions[session["index"]]
        logging.info(f"➡️ Sending Q{session['index'] + 1} to user {user_id}")
        await message.answer(
            f"{question}\n\nPlease reply with:\n0 = Not at all\n1 = Several days\n2 = More than half the days\n3 = Nearly every day"
        )
