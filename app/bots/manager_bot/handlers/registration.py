from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.utils.validators import is_valid_email, is_valid_phone
from app.db.models import PendingRegistration
from app.utils.logging import logger

router = Router()


class RegistrationSG(StatesGroup):
    waiting_name = State()
    waiting_email = State()
    waiting_phone = State()
    waiting_role = State()
    confirm = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать! Вы новый менеджер или уже зарегистрированы?\n\n"
        "Команды:\n/register — регистрация нового менеджера\n/help — справка"
    )


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(RegistrationSG.waiting_name)
    await message.answer("Введите ваше ФИО или отправьте /cancel для отмены")


@router.message(F.text, RegistrationSG.waiting_name)
async def state_name(message: Message, state: FSMContext):
    await state.update_data(
        name=message.text,
        telegram_username=message.from_user.username,
        telegram_id=message.from_user.id
    )
    await state.set_state(RegistrationSG.waiting_email)
    await message.answer("Введите ваш email")


@router.message(F.text, RegistrationSG.waiting_email)
async def state_email(message: Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer("Неверный email. Попробуйте еще раз или отправьте /cancel")
        return
    await state.update_data(email=message.text)
    await state.set_state(RegistrationSG.waiting_phone)
    await message.answer("Введите номер телефона")


@router.message(F.text, RegistrationSG.waiting_phone)
async def state_phone(message: Message, state: FSMContext):
    if not is_valid_phone(message.text):
        await message.answer("Неверный номер. Укажите в формате +79991234567 или 89991234567")
        return
    await state.update_data(phone=message.text)
    await state.set_state(RegistrationSG.waiting_role)
    await message.answer("Выберите роль: Junior, Middle или Senior. Введите текстом.")


@router.message(F.text, RegistrationSG.waiting_role)
async def state_role(message: Message, state: FSMContext):
    role = message.text.strip().lower()
    if role not in ("junior", "middle", "senior"):
        await message.answer("Роль должна быть: Junior, Middle или Senior")
        return
    await state.update_data(role=role)
    data = await state.get_data()
    text = (
        f"Проверьте данные:\n"
        f"👤 ФИО: {data.get('name')}\n"
        f"📧 Email: {data.get('email')}\n"
        f"📱 Телефон: {data.get('phone')}\n"
        f"💼 Роль: {data.get('role')}\n\n"
        "Отправьте 'Подтвердить' для отправки заявки или /cancel для отмены"
    )
    await state.set_state(RegistrationSG.confirm)
    await message.answer(text)


@router.message(F.text, RegistrationSG.confirm)
async def state_confirm(message: Message, state: FSMContext):
    if message.text.lower() != 'подтвердить':
        await message.answer("Отправьте 'Подтвердить' или /cancel")
        return
    
    data = await state.get_data()
    try:
        await PendingRegistration.create(
            telegram_id=data['telegram_id'],
            telegram_username=data.get('telegram_username'),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            role=data['role']
        )
        await message.answer("✅ Ваша заявка отправлена администратору. Ожидайте подтверждения.")
        # TODO: send notification to admin bot via internal mechanism
    except Exception as exc:
        logger.exception("Failed to create pending registration")
        await message.answer("❌ Произошла ошибка при создании заявки. Попробуйте позже.")
    finally:
        await state.clear()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Регистрация отменена")
