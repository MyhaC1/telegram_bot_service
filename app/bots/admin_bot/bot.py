from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from app.bots.admin_bot.handlers import pending, common


class BotHolder:
    def __init__(self):
        self._bot = None

    def set_bot(self, bot: Bot):
        self._bot = bot

    def get(self) -> Bot:
        return self._bot


_admin_bot_holder = BotHolder()


def get_admin_bot() -> BotHolder:
    return _admin_bot_holder


async def setup_admin_bot(storage: BaseStorage):
    from app.core.config import settings
    
    bot = Bot(token=settings.BOT_TOKEN_ADMIN)
    dp = Dispatcher(storage=storage)
    
    dp.include_router(pending.router)
    dp.include_router(common.router)
    
    return dp, bot
