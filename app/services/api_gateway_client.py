import httpx
from typing import Any, Dict, Optional, List
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

    # Pending Registrations
    async def create_pending_registration(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Создать pending регистрацию менеджера"""
        try:
            resp = await self.client.post(f"{self.base_url}/api/pending-registrations/", json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            logger.exception("API Gateway create_pending_registration failed")
            raise

    async def get_pending_registrations(self, status: str = "pending") -> List[Dict[str, Any]]:
        """Получить список pending регистраций"""
        try:
            resp = await self.client.get(f"{self.base_url}/api/pending-registrations/", params={"status": status})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            logger.exception("API Gateway get_pending_registrations failed")
            raise

    async def approve_registration(self, registration_id: int, admin_id: int) -> Dict[str, Any]:
        """Одобрить регистрацию"""
        try:
            resp = await self.client.post(
                f"{self.base_url}/api/pending-registrations/{registration_id}/approve",
                json={"admin_id": admin_id}
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            logger.exception("API Gateway approve_registration failed")
            raise

    async def reject_registration(self, registration_id: int, admin_id: int, reason: str) -> Dict[str, Any]:
        """Отклонить регистрацию"""
        try:
            resp = await self.client.post(
                f"{self.base_url}/api/pending-registrations/{registration_id}/reject",
                json={"admin_id": admin_id, "reason": reason}
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            logger.exception("API Gateway reject_registration failed")
            raise

    # Managers
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

    # Clients
    async def create_client(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self.client.post(f"{self.base_url}/api/clients/", json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            logger.exception("API Gateway create_client failed")
            raise


api_gateway_client = APIGatewayClient()
