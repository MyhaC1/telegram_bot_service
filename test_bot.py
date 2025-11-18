"""
Тестовый запуск бота без Redis (используется MemoryStorage для FSM)
Для быстрого тестирования без Docker
"""
from fastapi import FastAPI
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.core.database import init_db, close_db
from app.utils.logging import setup_logging
from app.bots.manager_bot.bot import setup_manager_bot, get_manager_bot
from app.bots.admin_bot.bot import setup_admin_bot, get_admin_bot

app = FastAPI(title="Telegram Bot Service (Test Mode)")


@app.on_event("startup")
async def startup():
    print("🚀 Starting Telegram Bot Service (Test Mode with MemoryStorage)...")
    setup_logging()

    # Tortoise
    print("📊 Initializing database...")
    await init_db()
    print("✅ Database initialized")

    # Memory storage for FSM (вместо Redis для тестирования)
    storage = MemoryStorage()
    print("💾 Using MemoryStorage (no Redis needed)")

    # Initialize bots and dispatchers
    print("🤖 Setting up Manager Bot...")
    manager_dp, manager_bot = await setup_manager_bot(storage=storage)
    print("✅ Manager Bot ready")
    
    print("🔧 Setting up Admin Bot...")
    admin_dp, admin_bot = await setup_admin_bot(storage=storage)
    print("✅ Admin Bot ready")

    # store bot instances (for other modules)
    get_manager_bot().set_bot(manager_bot)
    get_admin_bot().set_bot(admin_bot)

    # Start polling in background tasks
    print("🔄 Starting polling...")
    asyncio.create_task(manager_dp.start_polling(manager_bot))
    asyncio.create_task(admin_dp.start_polling(admin_bot))
    print("✅ Bots are running!")
    print(f"📱 Manager Bot: @{(await manager_bot.get_me()).username}")
    print(f"🔧 Admin Bot: @{(await admin_bot.get_me()).username}")


@app.on_event("shutdown")
async def shutdown():
    print("🛑 Shutting down...")
    await close_db()


@app.get("/")
async def root():
    return {
        "service": "telegram_bot_service",
        "mode": "test",
        "storage": "memory",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "telegram_bot_service", "mode": "test"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
