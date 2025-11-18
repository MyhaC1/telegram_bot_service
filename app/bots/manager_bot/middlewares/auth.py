from aiogram import BaseMiddleware
from aiogram.types import Message
from app.services.api_gateway_client import api_gateway_client
from app.utils.logging import logger


class ManagerAuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        # Check manager existence via API Gateway
        try:
            tg_id = event.from_user.id
            resp = await api_gateway_client.get_manager(tg_id)
            data['manager'] = resp
        except Exception as exc:
            logger.debug("Manager lookup failed or not found")
            data['manager'] = None
        return await handler(event, data)
