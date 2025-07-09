#!/usr/bin/env python3
"""
web_transcriber.py

A Flask web application wrapper around OpenAI's Whisper API.
Requires:
    pip install flask openai python-dotenv pydub ffmpeg-python
Usage:
    export OPENAI_API_KEY="sk-..."
    python web_app.py
"""

import os
import uuid
import math
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pydub import AudioSegment
import ffmpeg

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'ogg', 'webm', 'mp4'}

# Whisper API limits
WHISPER_MAX_SIZE = 25 * 1024 * 1024  # 25MB
CHUNK_DURATION = 10 * 60 * 1000  # 10 minutes in milliseconds

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """Get file size in bytes"""
    return os.path.getsize(file_path)

def compress_audio(audio_path: str, target_size_mb: int = 20) -> str:
    """Compress audio file to target size using ffmpeg"""
    try:
        # Get original file size
        original_size = get_file_size(audio_path)
        target_size = target_size_mb * 1024 * 1024
        
        if original_size <= target_size:
            return audio_path
        
        # Calculate bitrate based on target size and duration
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['format']['duration'])
        
        # Calculate bitrate (bits per second)
        # Leave some buffer for metadata
        target_bitrate = int((target_size * 8 * 0.95) / duration)
        
        # Ensure minimum quality (64kbps)
        target_bitrate = max(target_bitrate, 64000)
        
        # Create compressed file path
        base_name = os.path.splitext(audio_path)[0]
        compressed_path = f"{base_name}_compressed.mp3"
        
        # Compress using ffmpeg
        stream = ffmpeg.input(audio_path)
        stream = ffmpeg.output(stream, compressed_path, 
                             acodec='mp3', 
                             ab=target_bitrate,
                             ac=1,  # Mono audio (saves space)
                             ar=16000)  # 16kHz sample rate (Whisper optimal)
        
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        # Verify compression worked
        if os.path.exists(compressed_path) and get_file_size(compressed_path) <= target_size:
            return compressed_path
        else:
            return audio_path
            
    except Exception as e:
        print(f"Warning: Could not compress audio file: {e}")
        return audio_path

def chunk_audio(audio_path: str) -> list:
    """Split audio file into chunks of 10 minutes each"""
    try:
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio)
        
        if duration <= CHUNK_DURATION:
            return [audio_path]
        
        chunks = []
        num_chunks = math.ceil(duration / CHUNK_DURATION)
        
        for i in range(num_chunks):
            start_time = i * CHUNK_DURATION
            end_time = min((i + 1) * CHUNK_DURATION, duration)
            
            chunk = audio[start_time:end_time]
            
            # Save chunk
            base_name = os.path.splitext(audio_path)[0]
            chunk_path = f"{base_name}_chunk_{i+1}.wav"
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
        
        return chunks
        
    except Exception as e:
        print(f"Warning: Could not chunk audio file: {e}")
        return [audio_path]

def trim_audio_to_10_minutes(audio_path: str) -> str:
    """Trim audio file to first 10 minutes and return path to trimmed file"""
    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Calculate 10 minutes in milliseconds
        ten_minutes = 10 * 60 * 1000
        
        # Trim to first 10 minutes if longer
        if len(audio) > ten_minutes:
            audio = audio[:ten_minutes]
        
        # Create trimmed file path
        base_name = os.path.splitext(audio_path)[0]
        trimmed_path = f"{base_name}_trimmed.wav"
        
        # Export as WAV (Whisper handles WAV well)
        audio.export(trimmed_path, format="wav")
        
        return trimmed_path
    except Exception as e:
        # If trimming fails, return original file
        print(f"Warning: Could not trim audio file: {e}")
        return audio_path

def transcribe_with_whisper(api_key: str, audio_path: str) -> str:
    """Transcribe audio file using OpenAI Whisper API"""
    client = OpenAI(api_key=api_key)
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def transcribe_with_whisper_verbose(api_key: str, audio_path: str):
    """Transcribe audio file using OpenAI Whisper API, return verbose JSON (segments)."""
    client = OpenAI(api_key=api_key)
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json"
        )
    return response

def segments_to_srt(segments):
    """Convert Whisper segments to SRT format string."""
    def format_timestamp(seconds):
        ms = int((seconds - int(seconds)) * 1000)
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    srt_lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()
        srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(srt_lines)

def transcribe_large_file(api_key: str, audio_path: str, trim_to_10min: bool = False) -> str:
    """Handle transcription of large files with compression and chunking"""
    try:
        # Step 1: Trim if requested
        if trim_to_10min:
            audio_path = trim_audio_to_10_minutes(audio_path)
        
        # Step 2: Check file size
        file_size = get_file_size(audio_path)
        
        if file_size <= WHISPER_MAX_SIZE:
            # File is small enough, transcribe directly
            return transcribe_with_whisper(api_key, audio_path)
        
        # Step 3: Compress the file
        compressed_path = compress_audio(audio_path)
        compressed_size = get_file_size(compressed_path)
        
        if compressed_size <= WHISPER_MAX_SIZE:
            # Compression worked, transcribe compressed file
            transcript = transcribe_with_whisper(api_key, compressed_path)
            # Clean up compressed file
            if compressed_path != audio_path:
                os.remove(compressed_path)
            return transcript
        
        # Step 4: File is still too large, need to chunk
        chunks = chunk_audio(compressed_path)
        transcripts = []
        
        for i, chunk_path in enumerate(chunks):
            # Compress each chunk if needed
            chunk_size = get_file_size(chunk_path)
            if chunk_size > WHISPER_MAX_SIZE:
                compressed_chunk = compress_audio(chunk_path)
                chunk_path = compressed_chunk
            
            # Transcribe chunk
            chunk_transcript = transcribe_with_whisper(api_key, chunk_path)
            transcripts.append(f"[Part {i+1}]\n{chunk_transcript}")
            
            # Clean up chunk file
            if chunk_path != audio_path:
                os.remove(chunk_path)
        
        # Clean up compressed file
        if compressed_path != audio_path:
            os.remove(compressed_path)
        
        return "\n\n".join(transcripts)
        
    except Exception as e:
        raise Exception(f"Error processing large file: {str(e)}")

def transcribe_large_file_with_srt(api_key: str, audio_path: str, trim_to_10min: bool = False):
    """Transcribe and return both plain text and SRT (segments)."""
    try:
        if trim_to_10min:
            audio_path = trim_audio_to_10_minutes(audio_path)
        file_size = get_file_size(audio_path)
        if file_size <= WHISPER_MAX_SIZE:
            response = transcribe_with_whisper_verbose(api_key, audio_path)
            transcript = response.text
            segments = response.segments
            return transcript, segments
        compressed_path = compress_audio(audio_path)
        compressed_size = get_file_size(compressed_path)
        if compressed_size <= WHISPER_MAX_SIZE:
            response = transcribe_with_whisper_verbose(api_key, compressed_path)
            transcript = response.text
            segments = response.segments
            if compressed_path != audio_path:
                os.remove(compressed_path)
            return transcript, segments
        chunks = chunk_audio(compressed_path)
        transcripts = []
        all_segments = []
        for i, chunk_path in enumerate(chunks):
            chunk_size = get_file_size(chunk_path)
            if chunk_size > WHISPER_MAX_SIZE:
                compressed_chunk = compress_audio(chunk_path)
                chunk_path = compressed_chunk
            response = transcribe_with_whisper_verbose(api_key, chunk_path)
            transcripts.append(f"[Part {i+1}]\n{response.text}")
            all_segments.extend(response.segments)
            if chunk_path != audio_path:
                os.remove(chunk_path)
        if compressed_path != audio_path:
            os.remove(compressed_path)
        return "\n\n".join(transcripts), all_segments
    except Exception as e:
        raise Exception(f"Error processing large file: {str(e)}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Handle file upload and transcription, and generate SRT."""
    try:
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['audio_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an audio file.'}), 400
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        trim_to_10min = request.form.get('trim_to_10min') == 'true'
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        # Transcribe and get segments
        transcript, segments = transcribe_large_file_with_srt(api_key, file_path, trim_to_10min)
        # Save transcript as text file
        txt_filename = f"{os.path.splitext(unique_filename)[0]}.txt"
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        # Save SRT file
        srt_filename = f"{os.path.splitext(unique_filename)[0]}.srt"
        srt_path = os.path.join(app.config['UPLOAD_FOLDER'], srt_filename)
        srt_content = segments_to_srt(segments)
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        os.remove(file_path)
        return jsonify({
            'transcript': transcript,
            'download_url': f'/download/{txt_filename}',
            'filename': txt_filename,
            'trimmed': trim_to_10min,
            'srt_url': f'/download/{srt_filename}',
            'srt_filename': srt_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download transcribed text file"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 