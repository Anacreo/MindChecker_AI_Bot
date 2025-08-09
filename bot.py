import os
import json
from datetime import datetime, timezone
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

DATA_FILE = "user_data.json"

# Load/save user data
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

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

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name or "there"
    user_data = load_user_data()
    now_str = datetime.now(timezone.utc).isoformat()

    if user_id in user_data:
        ago = time_since(user_data[user_id]["last_seen"])
        message = f"👋 Welcome back, {user_name}! It's been {ago} since we last saw you."
    else:
        message = f"👋 Hello, {user_name}! Nice to meet you."

    user_data[user_id] = {"last_seen": now_str}
    save_user_data(user_data)
    await update.message.reply_text(message)

# Telegram bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"

bot_app = Application.builder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# Webhook route
async def telegram_webhook(request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return Response()

# Health check route
async def health_check(request):
    return Response("OK")

# Starlette app
routes = [
    Route("/webhook", telegram_webhook, methods=["POST"]),
    Route("/", health_check, methods=["GET"]),
]
app = Starlette(debug=True, routes=routes)

# Set webhook on startup
@app.on_event("startup")
async def startup():
    await bot_app.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")
