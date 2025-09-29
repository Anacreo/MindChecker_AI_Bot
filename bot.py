import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8443))  # Render sets PORT dynamically

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FastAPI app
app = FastAPI()

# Webhook route
@app.post("/webhook")
async def webhook_handler(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return JSONResponse(content={"ok": True})

# Startup hook to set webhook
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

# Optional shutdown hook
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    logging.info("Webhook removed")

# Uvicorn entry point for Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=PORT)
