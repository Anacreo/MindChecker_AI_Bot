import logging
import os
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from contextlib import asynccontextmanager

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
register_all_handlers(dp)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Starting bot...")
    await bot.set_webhook(WEBHOOK_URL)
    yield
    logging.info("🛑 Shutting down bot...")
    await bot.delete_webhook()

# FastAPI app
app = FastAPI(lifespan=lifespan)

# Optional health check route
@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Webhook binding
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)
