#!/usr/bin/env python3
"""
OpenAI Whisper Transcription Script
Supports both API and Local modes
"""

import os
import sys
from pathlib import Path

def transcribe_with_api(audio_file, api_key=None):
    """Transcribe using OpenAI Whisper API (paid)"""
    from openai import OpenAI

    # Get API key from environment or parameter
    api_key = api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found")
        print("   Set it with: export OPENAI_API_KEY='your-api-key'")
        return None

    client = OpenAI(api_key=api_key)

    print(f"🎙️  Transcribing with OpenAI Whisper API...")
    print(f"   File: {audio_file}")

    try:
        with open(audio_file, 'rb') as audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                response_format="verbose_json",  # Get timestamps
                timestamp_granularities=["word"]
            )

        print(f"\n✅ Transcription complete!")
        print(f"\n📝 Transcript:\n")
        print(transcript.text)

        # Save to file
        output_file = Path(audio_file).stem + "_transcript.txt"
        with open(output_file, 'w') as f:
            f.write(transcript.text)
        print(f"\n💾 Saved to: {output_file}")

        return transcript.text

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def transcribe_with_local(audio_file):
    """Transcribe using local Whisper (free, requires faster-whisper)"""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("❌ faster-whisper not installed")
        print("   Install with: pip3 install faster-whisper")
        return None

    print(f"🎙️  Transcribing with Local Whisper...")
    print(f"   File: {audio_file}")
    print(f"   Loading model (this may take a moment)...")

    try:
        # Use base model (good balance of speed and accuracy)
        # Options: tiny, base, small, medium, large-v3
        model = WhisperModel("base", device="cpu", compute_type="int8")

        segments, info = model.transcribe(
            audio_file,
            word_timestamps=True,
            vad_filter=True  # Voice activity detection
        )

        print(f"   Language: {info.language} ({info.language_probability:.2%} confidence)")
        print(f"\n✅ Transcription complete!")
        print(f"\n📝 Transcript:\n")

        full_text = []
        for segment in segments:
            text = segment.text.strip()
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {text}")
            full_text.append(text)

        # Save to file
        transcript = " ".join(full_text)
        output_file = Path(audio_file).stem + "_transcript.txt"
        with open(output_file, 'w') as f:
            f.write(transcript)
        print(f"\n💾 Saved to: {output_file}")

        return transcript

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Option 1 - API (paid):   python3 whisper_transcribe.py audio.mp3 --api")
        print("  Option 2 - Local (free): python3 whisper_transcribe.py audio.mp3 --local")
        print("\nFor API mode, set OPENAI_API_KEY environment variable")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not os.path.exists(audio_file):
        print(f"❌ Error: File not found: {audio_file}")
        sys.exit(1)

    # Determine mode
    mode = "--api" if "--api" in sys.argv else "--local"

    print("=" * 60)
    print("🎤 WHISPER TRANSCRIPTION")
    print("=" * 60)

    if mode == "--api":
        transcribe_with_api(audio_file)
    else:
        transcribe_with_local(audio_file)


if __name__ == "__main__":
    main()
