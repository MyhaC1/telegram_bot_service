from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.db.models import PendingRegistration
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
        "/managers — управление менеджерами\n"
        "/help — справка"
    )


@router.message(Command("pending"))
async def cmd_pending(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⛔ У вас нет доступа к этому боту")
        return

    items = await PendingRegistration.filter(status="pending").order_by("-created_at")
    if not items:
        await message.answer("📭 Нет ожидающих заявок")
        return

    for p in items:
        text = (
            f"📋 Заявка #{p.id}\n"
            f"👤 ФИО: {p.name}\n"
            f"📧 Email: {p.email}\n"
            f"📱 Телефон: {p.phone}\n"
            f"💼 Роль: {p.role}\n"
            f"📅 Дата: {p.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Для одобрения: approve {p.id}\n"
            f"Для отклонения: reject {p.id} причина"
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
            pid = int(parts[1])
            p = await PendingRegistration.get_or_none(id=pid)
            if not p:
                await message.answer("❌ Заявка не найдена")
                return
            
            # create manager via API Gateway
            data = {
                "telegram_id": p.telegram_id,
                "name": p.name,
                "email": p.email,
                "phone": p.phone,
                "role": p.role,
                "is_active": True,
            }
            
            try:
                await api_gateway_client.create_manager(data)
            except Exception as exc:
                logger.exception("Failed to create manager via API Gateway")
                await message.answer("❌ Ошибка при создании менеджера через API Gateway")
                return
            
            p.status = "approved"
            p.processed_by_admin_id = message.from_user.id
            await p.save()
            
            # notify manager via manager bot
            mgr_bot = get_manager_bot().get()
            if mgr_bot:
                try:
                    await mgr_bot.send_message(p.telegram_id, "✅ Ваша регистрация одобрена!")
                except Exception as exc:
                    logger.exception("Failed to notify manager")
            
            await message.answer(f"✅ Заявка #{p.id} одобрена")
            
        except ValueError:
            await message.answer("❌ Неверный id")
        except Exception as exc:
            logger.exception("Error approving registration")
            await message.answer("❌ Ошибка при обработке заявки")
    
    elif cmd == "reject" and len(parts) >= 2:
        try:
            pid = int(parts[1])
            reason = " ".join(parts[2:]) if len(parts) > 2 else "не указана"
            
            p = await PendingRegistration.get_or_none(id=pid)
            if not p:
                await message.answer("❌ Заявка не найдена")
                return
            
            p.status = "rejected"
            p.rejection_reason = reason
            p.processed_by_admin_id = message.from_user.id
            await p.save()
            
            # notify
            mgr_bot = get_manager_bot().get()
            if mgr_bot:
                try:
                    text = f"❌ Ваша регистрация отклонена. Причина: {reason}"
                    await mgr_bot.send_message(p.telegram_id, text)
                except Exception as exc:
                    logger.exception("Failed to notify manager about rejection")
            
            await message.answer(f"❌ Заявка #{p.id} отклонена")
            
        except ValueError:
            await message.answer("❌ Неверный id")
        except Exception as exc:
            logger.exception("Error rejecting registration")
            await message.answer("❌ Ошибка при обработке заявки")
