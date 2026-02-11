#!/usr/bin/env python3
"""
Einfacher STT Audio-Recorder
Direkt im Terminal - kein Browser nötig!
"""

import sounddevice as sd
import numpy as np
import wave
import subprocess
import tempfile
import os
import sys

SAMPLE_RATE = 16000
WHISPER_DIR = "/Users/developer/whisper.cpp"
MODEL = f"{WHISPER_DIR}/models/ggml-small.en.bin"

def record_audio(duration=5):
    """Nimmt Audio für X Sekunden auf"""
    print(f"🎙️  Aufnahme startet in 1 Sekunde...")
    print(f"⏱️  Dauer: {duration} Sekunden")
    print("")

    import time
    time.sleep(1)

    print("🔴 JETZT SPRECHEN!")
    print("=" * 50)

    # Record audio
    recording = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )

    sd.wait()  # Wait until recording is finished

    print("=" * 50)
    print("✅ Aufnahme beendet!")

    return recording

def save_wav(recording, filename):
    """Speichert Aufnahme als WAV-Datei"""
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())

def transcribe(wav_file, language='en'):
    """Transkribiert die Audio-Datei"""
    print(f"\n⏳ Transkribiere ({language})...")

    # Determine model
    if language == 'en':
        model = f"{WHISPER_DIR}/models/ggml-small.en.bin"
    else:
        model = f"{WHISPER_DIR}/models/ggml-base.bin"

    if not os.path.exists(model):
        model = f"{WHISPER_DIR}/models/ggml-base.bin"

    output_base = wav_file.replace('.wav', '')

    # Run whisper
    cmd = [
        f"{WHISPER_DIR}/build/bin/whisper-cli",
        "-m", model,
        "-f", wav_file,
        "-l", language,
        "-ng",  # No GPU
        "-otxt",
        "-of", output_base,
        "-np", "-nt"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    # Read result
    output_file = f"{output_base}.txt"
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        os.remove(output_file)
        return text

    return None

def main():
    print("=" * 50)
    print("🎙️  STT Audio Recorder")
    print("=" * 50)
    print("")

    # Language selection
    print("Wähle Sprache:")
    print("  1. 🇩🇪 Deutsch")
    print("  2. 🇬🇧 English")
    print("  3. 🇫🇷 Français")
    print("  4. 🇪🇸 Español")
    print("")

    choice = input("Deine Wahl (1-4): ").strip()

    language_map = {
        '1': 'de',
        '2': 'en',
        '3': 'fr',
        '4': 'es'
    }

    language = language_map.get(choice, 'en')

    # Duration
    print("")
    duration = input("Aufnahme-Dauer in Sekunden (Standard: 5): ").strip()
    try:
        duration = int(duration) if duration else 5
    except:
        duration = 5

    print("")

    # Record
    recording = record_audio(duration)

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        save_wav(recording, tmp.name)
        wav_file = tmp.name

    # Transcribe
    try:
        text = transcribe(wav_file, language)

        print("")
        print("=" * 50)
        print("📝 TRANSKRIPTION:")
        print("=" * 50)
        if text:
            print(text)
        else:
            print("❌ Keine Transkription generiert")
        print("=" * 50)
    finally:
        # Cleanup
        if os.path.exists(wav_file):
            os.remove(wav_file)

    print("")
    print("✅ Fertig!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Abgebrochen!")
        sys.exit(0)
