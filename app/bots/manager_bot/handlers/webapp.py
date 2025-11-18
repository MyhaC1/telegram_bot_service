from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
import json

from app.db.models import PendingRegistration
from app.utils.logging import logger
from app.core.config import settings
from app.utils.validators import is_valid_email, is_valid_phone, is_valid_date
from datetime import date

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    # Кнопка для открытия WebApp
    webapp_url = settings.WEBAPP_URL if hasattr(settings, 'WEBAPP_URL') else "https://YOUR_GITHUB_USERNAME.github.io/telegram_bot_service/webapp/"
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="📝 Зарегистрироваться",
                web_app=WebAppInfo(url=webapp_url)
            )],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я помогу вам зарегистрироваться как менеджер.\n\n"
        "Нажмите кнопку ниже для начала регистрации:",
        reply_markup=keyboard
    )


@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Обработка данных из Telegram Mini App"""
    try:
        # Парсим данные из WebApp
        data = json.loads(message.web_app_data.data)
        
        logger.info(f"Received WebApp data: {data}")
        
        # Проверяем что все поля заполнены
        required_fields = ['name', 'email', 'phone', 'role', 'birth_date']
        if not all(field in data for field in required_fields):
            await message.answer("❌ Ошибка: не все поля заполнены")
            return

        # Валидация полей
        if not is_valid_email(data.get('email')):
            await message.answer("❌ Некорректный email")
            return
        if not is_valid_phone(data.get('phone')):
            await message.answer("❌ Некорректный номер телефона")
            return
        if not is_valid_date(data.get('birth_date')):
            await message.answer("❌ Некорректная дата рождения")
            return

        # Разрешённые роли
        allowed_roles = {"sale", "reten", "admin", "lead"}
        role_value = str(data.get('role')).lower()
        if role_value not in allowed_roles:
            await message.answer("❌ Некорректная роль")
            return
        
        # Создаём pending регистрацию
        try:
            # Преобразуем дату рождения в объект date
            birth_date_val = None
            try:
                birth_date_val = date.fromisoformat(data.get('birth_date'))
            except Exception:
                birth_date_val = None

            pending = await PendingRegistration.create(
                telegram_id=message.from_user.id,
                telegram_username=message.from_user.username,
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                birth_date=birth_date_val,
                role=role_value,
                status='pending'
            )
            
            await message.answer(
                f"✅ Заявка #{pending.id} успешно отправлена!\n\n"
                f"👤 ФИО: {data['name']}\n"
                f"📧 Email: {data['email']}\n"
                f"📱 Телефон: {data['phone']}\n"
                f"💼 Роль: {data['role']}\n"
                f"🎂 Дата рождения: {data.get('birth_date')}\n\n"
                f"Администратор рассмотрит вашу заявку и уведомит о решении."
            )
            
            logger.info(f"Created pending registration #{pending.id} for user {message.from_user.id}")
            
        except Exception as db_error:
            logger.exception("Failed to create pending registration in database")
            
            # Проверяем если пользователь уже зарегистрирован
            existing = await PendingRegistration.filter(telegram_id=message.from_user.id).first()
            if existing:
                await message.answer(
                    f"⚠️ У вас уже есть заявка #{existing.id}\n"
                    f"Статус: {existing.status}\n\n"
                    f"Дождитесь решения администратора."
                )
            else:
                await message.answer("❌ Ошибка при сохранении заявки. Попробуйте позже.")
    
    except json.JSONDecodeError:
        logger.exception("Failed to parse WebApp data")
        await message.answer("❌ Ошибка обработки данных")
    except Exception as e:
        logger.exception("Error handling WebApp data")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    await message.answer(
        "📖 Справка:\n\n"
        "1️⃣ Нажмите кнопку 'Зарегистрироваться'\n"
        "2️⃣ Заполните форму регистрации\n"
        "3️⃣ Отправьте заявку\n"
        "4️⃣ Дождитесь одобрения администратора\n\n"
        "После одобрения вы получите уведомление и сможете работать с клиентами."
    )
