import json
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from handlers.phq9_classifier import classify_response 

# Load PHQ-9 questions from questionnaires/
with open("questionnaires/phq9.json", "r") as f:
    PHQ9 = json.load(f)

# In-memory session tracking
user_sessions = {}

# /phq9 command handler
async def phq9_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_sessions[user_id] = {"index": 0, "answers": []}
    await update.message.reply_text("🧠 Let's begin the PHQ-9 questionnaire.")
    await send_next_question(update, context)

# Send the current question
async def send_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session = user_sessions.get(user_id)

    if session is None:
        await update.message.reply_text("Please start with /phq9.")
        return

    index = session["index"]
    if index >= len(PHQ9):
        await update.message.reply_text("✅ Questionnaire complete. Thank you!")
        return

    question_text = PHQ9[index]["text"]
    await update.message.reply_text(f"**Question {index + 1}:**\n{question_text}")

# Handle user response to a question
async def phq9_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session = user_sessions.get(user_id)

    if session is None:
        await update.message.reply_text("Please start with /phq9.")
        return

    user_input = update.message.text

    try:
        classification = classify_response(user_input)
    except Exception as e:
        await update.message.reply_text("⚠️ Sorry, I couldn't process that. Please try again.")
        return

    session["answers"].append(classification)
    session["index"] += 1

    await update.message.reply_text(f"✅ Got it: *{classification}*")
    await send_next_question(update, context)

# Handlers to register in bot.py
phq9_start_handler = CommandHandler("phq9", phq9_start)
phq9_response_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, phq9_response)
