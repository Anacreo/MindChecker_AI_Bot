import json
import os
from datetime import datetime, timezone
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers.phq9 import phq9_start_handler, phq9_response_handler

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com
PORT = int(os.getenv("PORT", 8443))     # Render sets PORT env var

DATA_FILE = "user_data.json"

# Load user data from file
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user data to file
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Convert timestamp to relative time string
def time_since(timestamp_str):
    last_seen = datetime.fromisoformat(timestamp_str)
    now = datetime.now(timezone.utc)
    delta = now - last_seen

    seconds = int(delta.total_seconds())
    if seconds < 60:
        return f"{seconds} seconds ago"
    elif seconds < 3600:
        return f"{seconds // 60} minutes ago"
    elif seconds < 86400:
        return f"{seconds // 3600} hours ago"
    else:
        return f"{seconds // 86400} days ago"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name or "there"

    user_data = load_user_data()
    now_str = datetime.now(timezone.utc).isoformat()

    if user_id in user_data:
        last_seen = user_data[user_id]["last_seen"]
        ago = time_since(last_seen)
        message = f"👋 Welcome back, {user_name}! It's been {ago} since we last saw you."
    else:
        message = f"👋 Hello, {user_name}! Nice to meet you."

    # Update last seen
    user_data[user_id] = {"last_seen": now_str}
    save_user_data(user_data)

    await update.message.reply_text(message)

# Main bot setup
if __name__ == '__main__':
    bot = Bot(TOKEN)
    bot.delete_webhook()  # Clean up any old webhook
    bot.set_webhook(url=WEBHOOK_URL)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(phq9_start_handler)
    app.add_handler(phq9_response_handler)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )
