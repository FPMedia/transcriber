#!/usr/bin/env python3
"""
Windows setup script for Whisper Transcriber
This script helps set up the application on Windows systems
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ FFmpeg is available")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠ FFmpeg not found in PATH")
    print("Please install FFmpeg from: https://ffmpeg.org/download.html#build-windows")
    print("Add C:\\ffmpeg\\bin to your PATH environment variable")
    return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Directory '{directory}' ready")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write("OPENAI_API_KEY=your-api-key-here\n")
            f.write("SECRET_KEY=dev-secret-key-change-in-production\n")
        print("✓ Created .env file template")
        print("⚠ Please edit .env file and add your OpenAI API key")
    else:
        print("✓ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        # Use requirements.txt if it exists, otherwise use requirements_windows.txt
        req_file = 'requirements.txt' if Path('requirements.txt').exists() else 'requirements_windows.txt'
        
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', req_file], 
                      check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("Whisper Transcriber - Windows Setup")
    print("=" * 50)
    print()
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_ffmpeg():
        print("Continuing setup without FFmpeg...")
        print("Audio processing may not work properly without FFmpeg")
        print()
    
    # Create necessary directories
    create_directories()
    print()
    
    # Create environment file
    create_env_file()
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run: python web_app.py")
    print("3. Open your browser to: http://localhost:5000")
    print()
    print("Get your OpenAI API key from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
