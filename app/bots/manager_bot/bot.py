from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.base import BaseStorage
from app.bots.manager_bot.handlers import webapp, common


class BotHolder:
    def __init__(self):
        self._bot = None

    def set_bot(self, bot: Bot):
        self._bot = bot

    def get(self) -> Bot:
        return self._bot


_manager_bot_holder = BotHolder()


def get_manager_bot() -> BotHolder:
    return _manager_bot_holder


async def setup_manager_bot(storage: BaseStorage):
    from app.core.config import settings
    
    bot = Bot(token=settings.BOT_TOKEN_MANAGER)
    dp = Dispatcher(storage=storage)
    
    # register handlers (WebApp handler должен быть первым!)
    dp.include_router(webapp.router)
    dp.include_router(common.router)
    
    return dp, bot
