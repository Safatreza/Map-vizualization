@echo off
echo ========================================
echo AboutWater Customer Map - Vercel Deploy
echo ========================================
echo.

echo Checking prerequisites...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Vercel CLI!
        pause
        exit /b 1
    )
)

echo ✅ Prerequisites check passed!
echo.

echo Starting Vercel deployment...
echo.

REM Deploy to Vercel
vercel --prod

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Deployment successful!
    echo.
    echo Your customer map is now live on Vercel!
    echo Share the URL with your colleagues.
    echo.
    echo Next steps:
    echo 1. Test the deployed app
    echo 2. Share the URL with your team
    echo 3. Add to company intranet/bookmarks
    echo.
) else (
    echo.
    echo ❌ Deployment failed!
    echo Check the error messages above.
    echo.
)

pause
