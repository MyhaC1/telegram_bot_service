# 🔐 Решение проблемы с push на GitHub

## Проблема
`git push` не работает — GitHub требует аутентификацию.

## Решение 1: Personal Access Token (рекомендуется для HTTPS)

### Шаг 1: Создайте токен на GitHub

1. Откройте: https://github.com/settings/tokens/new
2. Заполните форму:
   - **Note**: `Telegram Bot Service`
   - **Expiration**: 90 days (или No expiration)
   - **Select scopes**: отметьте **repo** (все галочки в разделе repo)
3. Нажмите **Generate token**
4. **ВАЖНО**: Скопируйте токен сразу! (вы не сможете увидеть его снова)
   - Пример токена: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Шаг 2: Используйте токен вместо пароля

```powershell
# Вариант А: Push с токеном (разовый)
git push https://ghp_ВАШ_ТОКЕН@github.com/MyxaC1/telegram_bot_service.git master

# Вариант Б: Обновите remote с токеном (сохранится)
git remote set-url origin https://ghp_ВАШ_ТОКЕН@github.com/MyxaC1/telegram_bot_service.git
git push -u origin master
```

---

## Решение 2: GitHub CLI (самый простой)

```powershell
# Установите GitHub CLI
winget install --id GitHub.cli

# Авторизуйтесь
gh auth login

# Выберите:
# - GitHub.com
# - HTTPS
# - Login with a web browser
# - Скопируйте код и откройте браузер

# После авторизации:
git push -u origin master
```

---

## Решение 3: SSH ключ (для постоянного использования)

### Шаг 1: Сгенерируйте SSH ключ

```powershell
ssh-keygen -t ed25519 -C "developer@patriotbot.local"
# Нажмите Enter 3 раза (без пароля)
```

### Шаг 2: Добавьте ключ на GitHub

```powershell
# Скопируйте публичный ключ
Get-Content ~\.ssh\id_ed25519.pub | clip
```

1. Откройте: https://github.com/settings/ssh/new
2. Title: `My PC`
3. Key: вставьте из буфера (Ctrl+V)
4. Нажмите **Add SSH key**

### Шаг 3: Измените remote на SSH

```powershell
git remote set-url origin git@github.com:MyxaC1/telegram_bot_service.git
git push -u origin master
```

---

## Быстрое решение (прямо сейчас)

Если нужно быстро запушить:

```powershell
# 1. Создайте токен: https://github.com/settings/tokens/new
# 2. Скопируйте токен
# 3. Выполните (замените ВАШ_ТОКЕН):

git remote set-url origin https://ВАШ_ТОКЕН@github.com/MyxaC1/telegram_bot_service.git
git push -u origin master
```

---

## После успешного push

Включите GitHub Pages:
1. https://github.com/MyxaC1/telegram_bot_service/settings/pages
2. Source: **master** → **/ (root)** → Save
3. Подождите 2-3 минуты

Ваш WebApp будет доступен:
```
https://myxac1.github.io/telegram_bot_service/webapp/
```

Обновите `.env`:
```env
WEBAPP_URL=https://myxac1.github.io/telegram_bot_service/webapp/
```
