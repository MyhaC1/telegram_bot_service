import re
from datetime import datetime


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15


def is_valid_telegram_id(tid: str) -> bool:
    try:
        _ = int(tid)
        return True
    except Exception:
        return False


def is_valid_date(date_str: str) -> bool:
    """Validate date in YYYY-MM-DD format, not in the future, and reasonable year (>=1900)."""
    if not date_str:
        return False
    try:
        dt = datetime.fromisoformat(date_str)
    except ValueError:
        return False
    now = datetime.now()
    if dt > now:
        return False
    if dt.year < 1900:
        return False
    return True
