@echo off
echo ========================================
echo   GitHub Repository Setup Helper
echo ========================================
echo.
echo Your GitHub username appears to be: MyxaC1
echo.
echo Option 1: Repository already exists
echo -----------------------------------------
echo If you already created the repository on GitHub:
echo.
echo 1. Go to: https://github.com/MyxaC1/telegram_bot_service
echo 2. If it exists, copy the HTTPS URL
echo 3. Run:
echo    git remote remove origin
echo    git remote add origin [paste URL here]
echo    git push -u origin master
echo.
echo.
echo Option 2: Create new repository
echo -----------------------------------------
echo 1. Go to: https://github.com/new
echo 2. Repository name: telegram_bot_service
echo 3. Visibility: PUBLIC (important!)
echo 4. Do NOT add README, .gitignore, or license
echo 5. Click "Create repository"
echo.
echo Then run these commands:
echo.
echo git remote remove origin
echo git remote add origin https://github.com/MyxaC1/telegram_bot_service.git
echo git push -u origin master
echo.
echo.
echo After successful push:
echo -----------------------------------------
echo 1. Go to repository Settings
echo 2. Click "Pages" in left menu
echo 3. Source: select "master" branch
echo 4. Folder: select "/ (root)"
echo 5. Click Save
echo 6. Wait 2-3 minutes
echo.
echo Your WebApp will be at:
echo https://myxac1.github.io/telegram_bot_service/webapp/
echo.
echo ========================================
pause
