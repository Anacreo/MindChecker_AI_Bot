import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
import uvicorn

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8443))  # Render sets PORT dynamically

# Bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FastAPI app
app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
    return JSONResponse(content={"ok": True})

@app.on_event("startup")
async def on_startup():
    try:
        await bot.delete_webhook()
        await bot.set_webhook(url=WEBHOOK_URL)
        logging.info(f"✅ Webhook set to {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"❌ Failed to set webhook: {e}")

@app.on_event("shutdown")
async def on_shutdown():
    try:
        await bot.delete_webhook()
        logging.info("🛑 Webhook removed")
    except Exception as e:
        logging.error(f"❌ Failed to remove webhook: {e}")

if __name__ == "__main__":
    try:
        logging.info(f"🚀 Starting bot on port {PORT}")
        uvicorn.run("bot:app", host="0.0.0.0", port=PORT)
    except Exception as e:
        logging.error(f"❌ Bot failed to start: {e}")
