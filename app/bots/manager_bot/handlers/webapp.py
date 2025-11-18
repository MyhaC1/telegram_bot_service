from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
import json

from app.db.models import PendingRegistration
from app.utils.logging import logger
from app.core.config import settings

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
        required_fields = ['name', 'email', 'phone', 'role']
        if not all(field in data for field in required_fields):
            await message.answer("❌ Ошибка: не все поля заполнены")
            return
        
        # Создаём pending регистрацию
        try:
            pending = await PendingRegistration.create(
                telegram_id=message.from_user.id,
                telegram_username=message.from_user.username,
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                role=data['role'].lower(),
                status='pending'
            )
            
            await message.answer(
                f"✅ Заявка #{pending.id} успешно отправлена!\n\n"
                f"👤 ФИО: {data['name']}\n"
                f"📧 Email: {data['email']}\n"
                f"📱 Телефон: {data['phone']}\n"
                f"💼 Роль: {data['role']}\n\n"
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
