from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    HOST: str = "0.0.0.0"
    PORT: int = 8002

    API_GATEWAY_URL: str = "http://api_gateway:8080"

    BOT_TOKEN_MANAGER: str
    BOT_TOKEN_ADMIN: str
    ADMIN_TELEGRAM_IDS: Optional[str] = ""
    
    # Telegram WebApp URL (GitHub Pages или ваш хостинг)
    WEBAPP_URL: str = "https://myhac1.github.io/telegram_bot_service/webapp/"

    USE_WEBHOOK: bool = False
    WEBHOOK_DOMAIN: Optional[str] = None
    WEBHOOK_PATH: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
