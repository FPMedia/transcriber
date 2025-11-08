@echo off
echo ========================================
echo  Whisper Transcriber - Windows Installer
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/windows/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if FFmpeg is installed
echo.
echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found in PATH
    echo.
    echo FFmpeg is required for audio processing.
    echo Please install FFmpeg:
    echo 1. Download from: https://ffmpeg.org/download.html#build-windows
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH environment variable
    echo 4. Restart Command Prompt
    echo.
    echo Continuing with installation anyway...
    echo.
) else (
    echo FFmpeg found:
    ffmpeg -version 2>&1 | findstr "ffmpeg version"
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
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

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file...
    echo OPENAI_API_KEY=your-api-key-here > .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your actual OpenAI API key
    echo You can get your API key from: https://platform.openai.com/api-keys
)

REM Create uploads directory
if not exist uploads (
    echo Creating uploads directory...
    mkdir uploads
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit the .env file and add your OpenAI API key
echo 2. Run start_windows.bat to start the application
echo 3. Open your browser to http://localhost:5000
echo.
echo Your OpenAI API key should look like: sk-...
echo Get it from: https://platform.openai.com/api-keys
echo.
pause
