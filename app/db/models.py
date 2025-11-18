from tortoise import fields, models


class PendingRegistration(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    telegram_username = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=20)
    role = fields.CharField(max_length=50)
    status = fields.CharField(max_length=20, default="pending")
    rejection_reason = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    processed_by_admin_id = fields.BigIntField(null=True)

    class Meta:
        table = "pending_registrations"


class BotSession(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(index=True)
    bot_type = fields.CharField(max_length=20)
    session_data = fields.JSONField(default=dict)
    is_active = fields.BooleanField(default=True)
    last_activity = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bot_sessions"
