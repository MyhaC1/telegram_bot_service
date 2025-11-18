from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
import json

from app.utils.logging import logger
from app.core.config import settings
from app.services.api_gateway_client import api_gateway_client

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    # Кнопка для открытия WebApp
    webapp_url = settings.WEBAPP_URL
    
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
    """Обработка данных из Telegram Mini App - отправка в API Gateway"""
    try:
        # Парсим данные из WebApp
        data = json.loads(message.web_app_data.data)
        
        logger.info(f"Received WebApp data from user {message.from_user.id}: {data}")
        
        # Проверяем что все обязательные поля заполнены
        required_fields = ['name', 'phone', 'role', 'birth_date']
        if not all(field in data for field in required_fields):
            await message.answer("❌ Ошибка: не все поля заполнены")
            return
        
        # Отправляем данные в API Gateway для создания pending регистрации
        try:
            manager_data = {
                "telegram_id": message.from_user.id,
                "telegram_username": message.from_user.username,
                "name": data['name'],
                "phone": data['phone'],
                "birth_date": data['birth_date'],
                "role": data['role'],
                "status": "pending"
            }
            
            # Создаем pending регистрацию через API Gateway
            result = await api_gateway_client.create_pending_registration(manager_data)
            
            await message.answer(
                f"✅ Заявка успешно отправлена!\n\n"
                f"👤 ФИО: {data['name']}\n"
                f" Телефон: {data['phone']}\n"
                f"🎂 Дата рождения: {data['birth_date']}\n"
                f"💼 Роль: {data['role']}\n\n"
                f"Администратор рассмотрит вашу заявку и уведомит о решении."
            )
            
            logger.info(f"Successfully created pending registration for user {message.from_user.id}")
            
        except Exception as api_error:
            logger.exception("Failed to create pending registration via API Gateway")
            await message.answer(
                "❌ Ошибка при отправке заявки. Попробуйте позже или обратитесь к администратору."
            )
    
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
