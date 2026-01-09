import logging
import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Bot and dispatcher
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "") + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Routers
from handlers.phq9 import router as phq9_router
from handlers.start import router as start_router
dp.include_router(phq9_router)
dp.include_router(start_router)
logging.info("Start router included")


# FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Starting bot...")
    await bot.set_webhook(WEBHOOK_URL)
    yield
    logging.info("🛑 Shutting down bot...s")
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

# Health check route
@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Webhook GET (Telegram checks this before accepting the webhook)
@app.get(WEBHOOK_PATH)
async def webhook_get():
    return {"status": "ok"}

# Webhook POST (Telegram sends updates here)
@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
