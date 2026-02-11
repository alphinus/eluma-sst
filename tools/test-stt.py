#!/usr/bin/env python3
"""Quick STT test with existing audio"""

import subprocess
import os

WHISPER_DIR = "/Users/developer/whisper.cpp"
TEST_AUDIO = "/tmp/test_speech.wav"

def test_transcribe():
    print("🎙️  STT TEST")
    print("=" * 50)
    print(f"📁 Audio: {TEST_AUDIO}")
    print("")

    if not os.path.exists(TEST_AUDIO):
        print("❌ Test-Audio nicht gefunden!")
        return

    print("⏳ Transkribiere...")

    # Run whisper
    model = f"{WHISPER_DIR}/models/ggml-small.en.bin"
    output_base = "/tmp/test_result"

    cmd = [
        f"{WHISPER_DIR}/build/bin/whisper-cli",
        "-m", model,
        "-f", TEST_AUDIO,
        "-l", "en",
        "-ng",
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

        print("")
        print("=" * 50)
        print("✅ ERGEBNIS:")
        print("=" * 50)
        print(text)
        print("=" * 50)

        os.remove(output_file)
        return True
    else:
        print("❌ Keine Transkription generiert")
        return False

if __name__ == '__main__':
    test_transcribe()
