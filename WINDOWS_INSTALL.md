# 🪟 Windows Installation Guide - Whisper Transcriber

This guide will help you install the Whisper Transcriber web application on Windows.

## Prerequisites

### 1. Python Installation
- Download Python 3.7+ from [python.org](https://www.python.org/downloads/windows/)
- **Important**: During installation, check "Add Python to PATH"
- Verify installation by opening Command Prompt and running:
  ```cmd
  python --version
  pip --version
  ```

### 2. FFmpeg Installation (Required for audio processing)
- Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
- Extract to `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to your Windows PATH:
  1. Open System Properties → Advanced → Environment Variables
  2. Edit the "Path" variable
  3. Add `C:\ffmpeg\bin`
  4. Restart Command Prompt
- Verify installation:
  ```cmd
  ffmpeg -version
  ```

### 3. OpenAI API Key
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Keep it ready for configuration

## Installation Methods

### Method 1: Quick Installation (Recommended)

1. **Download the project**:
   - Copy the entire `transcriber` folder to your Windows machine
   - Or clone if you have git: `git clone <repository-url>`

2. **Run the installation script**:
   - Double-click `install_windows.bat` (see below for creation)
   - This will automatically install dependencies and set up the environment

3. **Configure your API key**:
   - Edit the `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

4. **Start the application**:
   - Double-click `start_windows.bat`
   - Open your browser to `http://localhost:5000`

### Method 2: Manual Installation

1. **Open Command Prompt as Administrator**

2. **Navigate to the project directory**:
   ```cmd
   cd C:\path\to\transcriber
   ```

3. **Create a virtual environment** (recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```cmd
   echo OPENAI_API_KEY=your-api-key-here > .env
   ```

6. **Start the application**:
   ```cmd
   python web_app.py
   ```

## Windows-Specific Files

### install_windows.bat
```batch
@echo off
echo Installing Whisper Transcriber for Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found in PATH
    echo Please install FFmpeg and add it to your PATH
    echo Download from: https://ffmpeg.org/download.html#build-windows
    echo.
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo OPENAI_API_KEY=your-api-key-here > .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your actual OpenAI API key
)

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run start_windows.bat to start the application
echo.
pause
```

### start_windows.bat
```batch
@echo off
echo Starting Whisper Transcriber...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run install_windows.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo .env file not found. Creating template...
    echo OPENAI_API_KEY=your-api-key-here > .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your actual OpenAI API key
    echo Then run this script again.
    pause
    exit /b 1
)

REM Start the application
echo Starting web server...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python web_app.py
```

## Usage

1. **Start the application** using one of the methods above
2. **Open your browser** and go to `http://localhost:5000`
3. **Upload an audio file** by dragging and dropping or clicking to browse
4. **Click "Transcribe Audio"** to start the transcription
5. **Download the transcript** when complete

## Troubleshooting

### Common Issues

1. **"Python is not recognized"**
   - Install Python from python.org
   - Make sure to check "Add Python to PATH" during installation
   - Restart Command Prompt after installation

2. **"FFmpeg is not recognized"**
   - Download FFmpeg from ffmpeg.org
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your PATH environment variable
   - Restart Command Prompt

3. **"Module not found" errors**
   - Make sure you're in the project directory
   - Activate the virtual environment: `venv\Scripts\activate`
   - Install dependencies: `pip install -r requirements.txt`

4. **"OpenAI API key not configured"**
   - Edit the `.env` file
   - Add your API key: `OPENAI_API_KEY=your-actual-key-here`
   - Make sure there are no spaces around the `=`

5. **"Permission denied" errors**
   - Run Command Prompt as Administrator
   - Or try installing to a different directory

6. **Audio processing fails**
   - Ensure FFmpeg is properly installed and in PATH
   - Try with a smaller audio file first
   - Check that the audio file is not corrupted

### Getting Help

- Check the browser's developer console (F12) for error messages
- Verify your OpenAI API key is valid and has sufficient credits
- Try with a smaller audio file first
- Ensure all dependencies are properly installed

## Security Notes

- Never share your OpenAI API key
- The `.env` file contains sensitive information - don't commit it to version control
- The application runs locally and doesn't send data to external servers except OpenAI

## Performance Tips

- Use the "Trim to first 10 minutes" option for long files to save API costs
- The application automatically compresses large files
- Very large files are split into chunks for processing
- Consider using a wired internet connection for large file uploads

## Uninstallation

To remove the application:
1. Delete the project folder
2. Remove the virtual environment (if you want to clean up completely)
3. No system-wide changes are made during installation
