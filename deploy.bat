@echo off
echo ========================================
echo   Telegram Bot Service - Quick Deploy
echo ========================================
echo.

echo [1/5] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Download: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo ✓ Git installed

echo.
echo [2/5] Initializing repository...
if not exist .git (
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Git already initialized
)

echo.
echo [3/5] Adding files...
git add .
git status --short

echo.
echo [4/5] Creating commit...
git commit -m "Telegram Bot Service with Mini App" 2>nul
if errorlevel 1 (
    echo ! No changes to commit or already committed
) else (
    echo ✓ Commit created
)

echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Create repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/telegram_bot_service.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Enable GitHub Pages:
echo    Settings -^> Pages -^> Source: main -^> Save
echo.
echo 4. Update .env with your WebApp URL:
echo    WEBAPP_URL=https://YOUR_USERNAME.github.io/telegram_bot_service/webapp/
echo.
echo 5. Run bot:
echo    python test_bot.py
echo.
echo ========================================
pause
