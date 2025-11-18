from aiogram import BaseMiddleware
from aiogram.types import Message
from app.core.config import settings


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if not settings.ADMIN_TELEGRAM_IDS:
            data['is_admin'] = False
            return await handler(event, data)
        
        admin_ids = [int(x.strip()) for x in settings.ADMIN_TELEGRAM_IDS.split(",") if x.strip()]
        data['is_admin'] = event.from_user.id in admin_ids
        
        return await handler(event, data)
