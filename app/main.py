from fastapi import FastAPI
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.utils.logging import setup_logging
from app.bots.manager_bot.bot import setup_manager_bot, get_manager_bot
from app.bots.admin_bot.bot import setup_admin_bot, get_admin_bot

app = FastAPI(title="Telegram Bot Service")


@app.on_event("startup")
async def startup():
    setup_logging()

    # FSM storage (используем MemoryStorage, т.к. не храним состояния долго)
    storage = MemoryStorage()

    # Initialize bots and dispatchers
    manager_dp, manager_bot = await setup_manager_bot(storage=storage)
    admin_dp, admin_bot = await setup_admin_bot(storage=storage)

    # store bot instances (for other modules)
    get_manager_bot().set_bot(manager_bot)
    get_admin_bot().set_bot(admin_bot)

    # Start polling in background tasks if not using webhook
    if not settings.USE_WEBHOOK:
        asyncio.create_task(manager_dp.start_polling(manager_bot))
        asyncio.create_task(admin_dp.start_polling(admin_bot))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "telegram_bot_service"}
