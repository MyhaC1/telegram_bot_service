from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_admin_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню администратора"""
    keyboard = [
        [KeyboardButton(text="📝 Pending регистрации")],
        [KeyboardButton(text="👥 Менеджеры"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_pending_actions_keyboard(pending_id: int) -> InlineKeyboardMarkup:
    """Клавиатура действий для pending регистрации"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{pending_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{pending_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
