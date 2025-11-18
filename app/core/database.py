from tortoise import Tortoise
from app.core.config import settings


async def init_db():
    # Use DATABASE_URL from settings
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.db.models"]}
    )
    # Don't auto-generate schemas in production; for dev we can create
    if settings.ENVIRONMENT != "production":
        await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
