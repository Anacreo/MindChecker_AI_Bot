import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from questionnaires.phq9 import evaluate_phq9_responses, get_question, get_options

router = Router()

# In-memory session store
user_sessions = {}

@router.message(F.text == "/phq9")
async def phq9_start(message: Message, state: FSMContext):
    user = message.from_user
    user_id = str(user.id)
    user_sessions[user_id] = {"index": 0, "answers": []}

    logging.info(
        f"🧠 PHQ-9 started by user_id={user.id}, username={user.username}, "
        f"name={user.first_name} {user.last_name}, language={user.language_code}"
    )

    await message.answer(
        "🧠 Let's begin the PHQ-9 questionnaire.\nYou can cancel anytime with /cancel."
    )
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
        score = int(message.text.strip())
    except ValueError:
        logging.warning(f"❌ Invalid input from user {user_id}: {message.text}")
        await message.answer("Please respond with a number between 0 and 3.")
        return

    session["answers"].append(score)
    session["index"] += 1
    logging.info(f"📥 User {user_id} answered Q{session['index']}: {score}")

    if session["index"] < 9:
        await send_next_question(message)
    else:
        result = evaluate_phq9_responses(session["answers"])
        total_score = result["total_score"]
        severity = result["severity"]
        suicide_risk = result["suicide_risk"]

        logging.info(
            f"✅ PHQ-9 complete for user {user_id}. Score: {total_score}, Severity: {severity}, Suicide Risk: {suicide_risk}"
        )

        breakdown = "\n".join([f"Q{i+1}: {a}" for i, a in enumerate(session["answers"])])
        risk_note = (
            "⚠️ You may be at risk. Please consider speaking with a professional."
            if suicide_risk else ""
        )

        await message.answer(
            f"✅ PHQ-9 complete.\n"
            f"Your total score is: {total_score}\n"
            f"Severity: *{severity}*\n\n"
            f"{risk_note}\n\n"
            f"Here’s your response breakdown:\n{breakdown}"
        )

        del user_sessions[user_id]

@router.message(F.text == "/cancel")
async def cancel_phq9(message: Message):
    user_id = str(message.from_user.id)
    if user_id in user_sessions:
        del user_sessions[user_id]
        logging.info(f"❌ PHQ-9 cancelled by user {user_id}")
        await message.answer("❌ PHQ-9 session cancelled.")
    else:
        await message.answer("No active PHQ-9 session to cancel.")

async def send_next_question(message: Message):
    user_id = str(message.from_user.id)
    session = user_sessions.get(user_id)

    if session and session["index"] < 9:
        q_num = session["index"] + 1
        question = get_question(q_num)
        logging.info(f"➡️ Sending Q{q_num} to user {user_id}")
        await message.answer(
            f"{question}\n\nPlease reply with:\n0 = Not at all\n1 = Several days\n2 = More than half the days\n3 = Nearly every day"
        )
