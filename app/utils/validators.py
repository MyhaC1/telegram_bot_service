import re


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
