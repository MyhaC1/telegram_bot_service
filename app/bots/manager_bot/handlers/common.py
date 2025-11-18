from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 Справка по командам:\n\n"
        "/start — приветствие и начало работы\n"
        "/register — регистрация нового менеджера\n"
        "/cancel — отмена текущей операции\n"
        "/help — эта справка"
    )
