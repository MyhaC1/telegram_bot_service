import logging
from pythonjsonlogger import jsonlogger
from app.core.config import settings


def setup_logging():
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL)
    if not root.handlers:
        root.addHandler(logHandler)


logger = logging.getLogger("telegram_bot_service")
