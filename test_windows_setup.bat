@echo off
echo ========================================
echo  Testing Windows Setup
echo ========================================
echo.

REM Test Python installation
echo Testing Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found
    echo Please install Python from: https://www.python.org/downloads/windows/
    echo Make sure to check "Add Python to PATH" during installation
) else (
    echo ✓ Python found:
    python --version
)

echo.

REM Test FFmpeg installation
echo Testing FFmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ✗ FFmpeg not found
    echo Please install FFmpeg from: https://ffmpeg.org/download.html#build-windows
    echo Add C:\ffmpeg\bin to your PATH environment variable
) else (
    echo ✓ FFmpeg found:
    ffmpeg -version 2>&1 | findstr "ffmpeg version"
)

echo.

REM Test virtual environment
echo Testing virtual environment...
if exist venv (
    echo ✓ Virtual environment exists
    call venv\Scripts\activate.bat >nul 2>&1
    if errorlevel 1 (
        echo ✗ Virtual environment is corrupted
        echo Please delete the 'venv' folder and run install_windows.bat again
    ) else (
        echo ✓ Virtual environment is working
    )
) else (
    echo ✗ Virtual environment not found
    echo Please run install_windows.bat first
)

echo.

REM Test .env file
echo Testing .env file...
if exist .env (
    echo ✓ .env file exists
    findstr /C:"your-api-key-here" .env >nul
    if not errorlevel 1 (
        echo ⚠ Default API key found - please update with your actual key
    ) else (
        echo ✓ API key appears to be configured
    )
) else (
    echo ✗ .env file not found
    echo Please run install_windows.bat first
)

echo.

REM Test dependencies
echo Testing Python dependencies...
if exist venv (
    call venv\Scripts\activate.bat >nul 2>&1
    python -c "import flask, openai, pydub" >nul 2>&1
    if errorlevel 1 (
        echo ✗ Dependencies not properly installed
        echo Please run install_windows.bat again
    ) else (
        echo ✓ All dependencies are installed
    )
) else (
    echo ✗ Cannot test dependencies - virtual environment not found
)

echo.

REM Test uploads directory
echo Testing uploads directory...
if exist uploads (
    echo ✓ Uploads directory exists
) else (
    echo ⚠ Uploads directory not found (will be created automatically)
)

echo.
echo ========================================
echo  Test Complete
echo ========================================
echo.

REM Check if everything is ready
if exist venv if exist .env (
    echo 🎉 Setup appears to be complete!
    echo.
    echo You can now:
    echo 1. Edit .env file to add your OpenAI API key
    echo 2. Run start_windows.bat to start the application
    echo 3. Open http://localhost:5000 in your browser
) else (
    echo ⚠ Setup is incomplete
    echo.
    echo Please:
    echo 1. Run install_windows.bat to complete installation
    echo 2. Edit .env file to add your OpenAI API key
    echo 3. Run start_windows.bat to start the application
)

echo.
pause
