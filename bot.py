import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm MindChecker AI Bot. How can I assist you today?\n\nFind me at: https://t.me/MindChecker_AI_Bot"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can ask me mental health questions, or type /check to start a mental health check!"
    )

def main():
    application = ApplicationBuilder().token('8489671487:AAHRtLdxt5AhrjaM8HYcSMNkJNLg19AJL_k').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()