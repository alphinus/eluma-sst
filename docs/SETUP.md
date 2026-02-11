# 🎤 OpenAI Whisper Setup Complete!

You now have TWO options for speech-to-text transcription:

## Option 1: Whisper API (Paid - uses your OpenAI account) ✅

**Cost:** ~$0.006 per minute of audio

### Setup:
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Or add to ~/.zshrc for permanent setup:
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
```

### Usage:
```bash
python3 whisper_transcribe.py your_audio.mp3 --api
```

**Features:**
- ✅ Super fast (cloud processing)
- ✅ No local resources needed
- ✅ Supports 99 languages
- ✅ Works immediately
- 💰 Pay per use (~$0.36 per hour)

---

## Option 2: Local Whisper (FREE - runs on your computer) 🆓

**Cost:** FREE

### Setup (in progress):
```bash
# ffmpeg is currently installing... (~10-15 minutes)
# Once complete, install faster-whisper:
pip3 install faster-whisper
```

### Usage:
```bash
python3 whisper_transcribe.py your_audio.mp3 --local
```

**Features:**
- ✅ Completely FREE
- ✅ Works offline
- ✅ Supports 99 languages
- ✅ Privacy (everything local)
- ⏱️ Slower (CPU processing)
- 💻 Downloads models (~150MB-3GB)

---

## Quick Start Examples

### 1. Test with a sample audio file:
```bash
# Download a sample
curl -o test_audio.mp3 https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav

# Transcribe with API
python3 whisper_transcribe.py test_audio.mp3 --api

# Or with local (once ffmpeg finishes)
python3 whisper_transcribe.py test_audio.mp3 --local
```

### 2. Transcribe your own audio:
```bash
# Works with: mp3, wav, m4a, mp4, webm, etc.
python3 whisper_transcribe.py path/to/your/audio.mp3 --api
```

### 3. Batch transcribe multiple files:
```bash
# Using API
for file in *.mp3; do
    python3 whisper_transcribe.py "$file" --api
done

# Using local
for file in *.mp3; do
    python3 whisper_transcribe.py "$file" --local
done
```

---

## Model Sizes (for Local mode)

When using local mode, you can choose different model sizes in the script:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~75MB | Very Fast | Good |
| base | ~150MB | Fast | Better ⭐ (default) |
| small | ~500MB | Medium | Great |
| medium | ~1.5GB | Slow | Excellent |
| large-v3 | ~3GB | Very Slow | Best |

---

## Status Check

✅ Python 3.14 - Installed
✅ OpenAI SDK - Installed
✅ Transcription script - Created
⏳ ffmpeg - Installing (in progress)
⏳ faster-whisper - Will install after ffmpeg completes

---

## Get Your OpenAI API Key

If you don't have an OpenAI API key yet:

1. Go to https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Set it: `export OPENAI_API_KEY="sk-..."`

---

## Supported Audio Formats

- MP3, WAV, M4A, MP4
- WebM, OGG, FLAC
- And many more!

---

## Need Help?

Run the script without arguments to see usage:
```bash
python3 whisper_transcribe.py
```

Check if ffmpeg finished installing:
```bash
which ffmpeg
```
