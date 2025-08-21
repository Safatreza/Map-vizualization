@echo off
echo ========================================
echo AboutWater Customer Map - GitHub Upload
echo ========================================
echo.

echo This script will help you upload your project to GitHub
echo and then deploy it to Vercel.
echo.

echo Step 1: Cloning the existing repository...
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo Please install Git from: https://git-scm.com/
    echo.
    pause
    exit /b 1
)

REM Clone the existing repository
if exist "Map-vizualization" (
    echo Repository already exists. Removing old files...
    cd Map-vizualization
    rmdir /s /q .git
    cd ..
    rmdir /s /q Map-vizualization
)

echo Cloning https://github.com/Safatreza/Map-vizualization.git
git clone https://github.com/Safatreza/Map-vizualization.git
if %errorlevel% neq 0 (
    echo ❌ Failed to clone repository!
    echo Check your internet connection and GitHub access.
    pause
    exit /b 1
)

echo.
echo Step 2: Copying project files...
echo.

REM Copy all project files to the cloned directory
xcopy /E /I /Y * Map-vizualization\
if %errorlevel% neq 0 (
    echo ❌ Failed to copy files!
    pause
    exit /b 1
)

echo.
echo Step 3: Uploading to GitHub...
echo.

cd Map-vizualization

REM Initialize git and add files
git init
git add .
git commit -m "🚀 Add AboutWater Customer Map - Complete interactive map with Vercel deployment"

REM Add remote origin and push
git remote add origin https://github.com/Safatreza/Map-vizualization.git
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Successfully uploaded to GitHub!
    echo.
    echo Your repository is now available at:
    echo https://github.com/Safatreza/Map-vizualization
    echo.
    echo Next steps:
    echo 1. Deploy to Vercel using the deploy button in README.md
    echo 2. Or run: vercel --prod
    echo 3. Share the Vercel URL with your team
    echo.
) else (
    echo.
    echo ❌ Failed to upload to GitHub!
    echo You may need to authenticate or check permissions.
    echo.
)

cd ..
pause
