from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню менеджера"""
    keyboard = [
        [KeyboardButton(text="➕ Добавить клиента")],
        [KeyboardButton(text="📋 Мои клиенты"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_registration_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения регистрации"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="reg_confirm")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="reg_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
