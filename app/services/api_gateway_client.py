import httpx
from typing import Any, Dict, Optional
from app.core.config import settings
from app.utils.logging import logger


class APIGatewayClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or str(settings.API_GATEWAY_URL)
        self._client = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    async def create_manager(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self.client.post(f"{self.base_url}/api/managers/", json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            logger.exception("API Gateway create_manager failed")
            raise

    async def get_manager(self, telegram_id: int) -> Dict[str, Any]:
        try:
            resp = await self.client.get(f"{self.base_url}/api/managers/{telegram_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return {}
            logger.exception("API Gateway get_manager failed")
            raise

    async def update_manager(self, telegram_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self.client.patch(f"{self.base_url}/api/managers/{telegram_id}", json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            logger.exception("API Gateway update_manager failed")
            raise

    async def create_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self.client.post(f"{self.base_url}/api/clients/", json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            logger.exception("API Gateway create_client failed")
            raise


api_gateway_client = APIGatewayClient()
