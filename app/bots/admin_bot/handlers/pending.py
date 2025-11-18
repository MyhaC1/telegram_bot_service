from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.services.api_gateway_client import api_gateway_client
from app.bots.manager_bot.bot import get_manager_bot
from app.core.config import settings
from app.utils.logging import logger

router = Router()


def is_admin(user_id: int) -> bool:
    if not settings.ADMIN_TELEGRAM_IDS:
        return False
    ids = [int(x.strip()) for x in settings.ADMIN_TELEGRAM_IDS.split(",") if x.strip()]
    return user_id in ids


@router.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этому боту")
        return
    
    await message.answer(
        "🔧 Admin Bot\n\n"
        "Доступные команды:\n"
        "/pending — просмотр pending регистраций\n"
        "/help — справка"
    )


@router.message(Command("pending"))
async def cmd_pending(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этому боту")
        return

    try:
        items = await api_gateway_client.get_pending_registrations(status="pending")
    except Exception as exc:
        logger.exception("Failed to get pending registrations from API Gateway")
        await message.answer("❌ Ошибка при получении списка заявок")
        return

    if not items:
        await message.answer("📭 Нет ожидающих заявок")
        return

    for p in items:
        registration_id = p.get('id')
        name = p.get('name', 'N/A')
        phone = p.get('phone', 'N/A')
        role = p.get('role', 'N/A')
        birth_date = p.get('birth_date', '')
        created_at = p.get('created_at', '')
        telegram_id = p.get('telegram_id')
        
        birth_info = f"🎂 Дата рождения: {birth_date}\n" if birth_date else ""
        
        text = (
            f"📋 Заявка #{registration_id}\n"
            f"👤 ФИО: {name}\n"
            f" Телефон: {phone}\n"
            f"💼 Роль: {role}\n"
            f"{birth_info}"
            f"🆔 Telegram ID: {telegram_id}\n"
            f"📅 Дата: {created_at}\n\n"
            f"Для одобрения: approve {registration_id}\n"
            f"Для отклонения: reject {registration_id} причина"
        )
        await message.answer(text)


@router.message()
async def text_handler(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        return
    
    text = message.text.strip().lower()
    parts = text.split()
    
    if not parts:
        return
    
    cmd = parts[0]
    
    if cmd == "approve" and len(parts) >= 2:
        try:
            registration_id = int(parts[1])
            
            # Одобряем через API Gateway
            try:
                result = await api_gateway_client.approve_registration(
                    registration_id=registration_id,
                    admin_id=message.from_user.id
                )
                
                # Уведомляем менеджера
                telegram_id = result.get('telegram_id')
                if telegram_id:
                    mgr_bot = get_manager_bot().get()
                    if mgr_bot:
                        try:
                            await mgr_bot.send_message(telegram_id, "✅ Ваша регистрация одобрена!")
                        except Exception as exc:
                            logger.exception("Failed to notify manager")
                
                await message.answer(f"✅ Заявка #{registration_id} одобрена")
                
            except Exception as exc:
                logger.exception("Failed to approve registration via API Gateway")
                await message.answer("❌ Ошибка при одобрении заявки")
                return
            
        except ValueError:
            await message.answer("❌ Неверный id")
        except Exception as exc:
            logger.exception("Error approving registration")
            await message.answer("❌ Ошибка при обработке заявки")
    
    elif cmd == "reject" and len(parts) >= 2:
        try:
            registration_id = int(parts[1])
            reason = " ".join(parts[2:]) if len(parts) > 2 else "не указана"
            
            try:
                result = await api_gateway_client.reject_registration(
                    registration_id=registration_id,
                    admin_id=message.from_user.id,
                    reason=reason
                )
                
                # Уведомляем менеджера
                telegram_id = result.get('telegram_id')
                if telegram_id:
                    mgr_bot = get_manager_bot().get()
                    if mgr_bot:
                        try:
                            text_msg = f"❌ Ваша регистрация отклонена. Причина: {reason}"
                            await mgr_bot.send_message(telegram_id, text_msg)
                        except Exception as exc:
                            logger.exception("Failed to notify manager about rejection")
                
                await message.answer(f"❌ Заявка #{registration_id} отклонена")
                
            except Exception as exc:
                logger.exception("Failed to reject registration via API Gateway")
                await message.answer("❌ Ошибка при отклонении заявки")
                return
            
        except ValueError:
            await message.answer("❌ Неверный id")
        except Exception as exc:
            logger.exception("Error rejecting registration")
            await message.answer("❌ Ошибка при обработке заявки")
