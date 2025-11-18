from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 Справка Admin Bot:\n\n"
        "/start — главное меню\n"
        "/pending — просмотр pending регистраций\n"
        "/managers — управление менеджерами (TODO)\n"
        "/help — эта справка\n\n"
        "Команды для обработки заявок:\n"
        "approve <id> — одобрить заявку\n"
        "reject <id> <причина> — отклонить заявку"
    )
