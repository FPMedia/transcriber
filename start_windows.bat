@echo off
echo ========================================
echo  Starting Whisper Transcriber
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo.
    echo Please run install_windows.bat first to install the application
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found
    echo.
    echo Creating template .env file...
    echo OPENAI_API_KEY=your-api-key-here > .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your actual OpenAI API key
    echo You can get your API key from: https://platform.openai.com/api-keys
    echo.
    echo After adding your API key, run this script again.
    echo.
    pause
    exit /b 1
)

REM Check if API key is configured
findstr /C:"your-api-key-here" .env >nul
if not errorlevel 1 (
    echo WARNING: Default API key found in .env file
    echo.
    echo Please edit the .env file and add your actual OpenAI API key
    echo You can get your API key from: https://platform.openai.com/api-keys
    echo.
    echo After adding your API key, run this script again.
    echo.
    pause
    exit /b 1
)

REM Check if uploads directory exists
if not exist uploads (
    echo Creating uploads directory...
    mkdir uploads
)

echo Starting web server...
echo.
echo ========================================
echo  Application is starting...
echo ========================================
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================

REM Start the application
python web_app.py
