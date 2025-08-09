import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from storage.session import get_session, update_session
from storage.user_data import save_response
from questionnaires.phq9 import get_question, get_options

async def phq9_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    update_session(user_id, "phq9", 1)
    q = get_question(1)
    opts = get_options(1)
    await update.message.reply_text(q, reply_markup=ReplyKeyboardMarkup(opts, one_time_keyboard=True))

async def phq9_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session = get_session(user_id)
    q_num = session["current_question"]
    response = update.message.text
    save_response(user_id, "phq9", q_num, response)

    next_q = q_num + 1
    if next_q > 9:
        await update.message.reply_text("✅ Questionnaire complete. Thank you!")
        update_session(user_id, None, 0)
    else:
        update_session(user_id, "phq9", next_q)
        q = get_question(next_q)
        opts = get_options(next_q)
        await update.message.reply_text(q, reply_markup=ReplyKeyboardMarkup(opts, one_time_keyboard=True))

phq9_start_handler = CommandHandler("phq9", phq9_start)
phq9_response_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, phq9_response)
