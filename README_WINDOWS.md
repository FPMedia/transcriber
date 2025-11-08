# 🪟 Whisper Transcriber - Windows Quick Start

**The fastest way to get Whisper Transcriber running on Windows!**

## 🚀 Quick Installation (2 minutes)

### Step 1: Prerequisites
- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/windows/) (check "Add Python to PATH")
- **FFmpeg**: Download from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows) and add to PATH
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)

### Step 2: Install
1. **Download** this project to your Windows machine
2. **Double-click** `install_windows.bat`
3. **Wait** for installation to complete

### Step 3: Configure
1. **Edit** the `.env` file
2. **Replace** `your-api-key-here` with your actual OpenAI API key
3. **Save** the file

### Step 4: Run
1. **Double-click** `start_windows.bat`
2. **Open** your browser to `http://localhost:5000`
3. **Upload** an audio file and transcribe!

## 📁 What's Included

- `install_windows.bat` - Automated installer
- `start_windows.bat` - Easy launcher
- `setup_windows.py` - Python setup script
- `requirements_windows.txt` - Windows-specific dependencies
- `WINDOWS_INSTALL.md` - Detailed installation guide

## 🎯 Features

- ✅ **One-click installation** with batch scripts
- ✅ **Automatic dependency management**
- ✅ **Virtual environment setup**
- ✅ **Windows-optimized audio processing**
- ✅ **Error checking and validation**
- ✅ **User-friendly error messages**

## 🔧 Manual Installation

If you prefer manual installation:

```cmd
# 1. Open Command Prompt as Administrator
# 2. Navigate to project folder
cd C:\path\to\transcriber

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
echo OPENAI_API_KEY=your-api-key-here > .env

# 6. Start application
python web_app.py
```

## 🆘 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "Python not recognized" | Install Python and check "Add to PATH" |
| "FFmpeg not found" | Install FFmpeg and add to PATH |
| "Module not found" | Run `install_windows.bat` first |
| "API key error" | Edit `.env` file with your actual key |
| "Permission denied" | Run Command Prompt as Administrator |

### Getting Help

1. **Check the detailed guide**: `WINDOWS_INSTALL.md`
2. **Run the setup script**: `python setup_windows.py`
3. **Verify prerequisites**: Python, FFmpeg, API key
4. **Check error messages**: Look for specific error details

## 🎵 Supported Audio Formats

- MP3, WAV, M4A, FLAC, OGG, WEBM, MP4
- Automatic compression for large files
- Smart chunking for very large files
- Audio trimming to save API costs

## 🔒 Security

- All processing happens locally
- Only audio files are sent to OpenAI
- API key stored securely in `.env` file
- No data collection or tracking

## 📊 Performance

- **File size limit**: 100MB (auto-compressed to 25MB)
- **Processing**: Automatic optimization for Whisper
- **Chunking**: Large files split into 10-minute chunks
- **Trimming**: Optional 10-minute limit to save costs

## 🎉 You're Ready!

Once installed, you can:
- Transcribe any audio file
- Download transcripts as text files
- Use the web interface from any device
- Process multiple files in sequence

**Happy transcribing!** 🎤✨
