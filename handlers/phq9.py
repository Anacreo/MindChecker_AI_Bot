import logging
import os
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from handlers import register_all_handlers

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "") + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
register_all_handlers(dp)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    logging.info("🚀 Starting bot...")
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"🌐 Webhook set to {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("🛑 Shutting down bot...")
    await bot.delete_webhook()

# Attach aiogram to FastAPI
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)
