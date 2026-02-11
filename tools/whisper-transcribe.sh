#!/bin/bash
# Whisper.cpp Transkriptions-Skript (KOSTENLOS!)
# Verwendung: ./whisper-transcribe.sh audio.mp3 [sprache]

if [ -z "$1" ]; then
    echo "❌ Fehler: Keine Audiodatei angegeben"
    echo ""
    echo "Verwendung:"
    echo "  ./whisper-transcribe.sh audio.mp3 [sprache]"
    echo ""
    echo "Beispiele:"
    echo "  ./whisper-transcribe.sh audio.mp3          # Auto-Erkennung"
    echo "  ./whisper-transcribe.sh audio.mp3 de       # Deutsch"
    echo "  ./whisper-transcribe.sh audio.mp3 en       # Englisch"
    echo ""
    echo "Unterstützte Formate: mp3, wav, m4a, flac, ogg, etc."
    echo "Sprachen: de, en, fr, es, it, pt, nl, ru, ja, ko, zh, ..."
    echo ""
    echo "Modell ändern: MODEL=small ./whisper-transcribe.sh audio.mp3"
    exit 1
fi

AUDIO_FILE="$1"
LANGUAGE="${2:-auto}"  # Default to auto detection
MODEL="${MODEL:-base}"
WHISPER_DIR="/Users/developer/whisper.cpp"
MODEL_PATH="$WHISPER_DIR/models/ggml-$MODEL.bin"

# Check if audio file exists
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ Datei nicht gefunden: $AUDIO_FILE"
    exit 1
fi

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "📥 Modell '$MODEL' wird heruntergeladen..."
    cd "$WHISPER_DIR" && bash ./models/download-ggml-model.sh "$MODEL"
fi

echo "🎙️  Transkribiere: $AUDIO_FILE"
echo "📊 Modell: $MODEL"
echo "🌍 Sprache: $LANGUAGE"
echo ""

# Run transcription (CPU-only for better stability)
$WHISPER_DIR/build/bin/whisper-cli \
    -m "$MODEL_PATH" \
    -f "$AUDIO_FILE" \
    -l "$LANGUAGE" \
    -ng \
    -otxt \
    -of "${AUDIO_FILE%.*}" \
    --print-colors

if [ $? -eq 0 ]; then
    OUTPUT_FILE="${AUDIO_FILE%.*}.txt"
    echo ""
    echo "✅ Transkription fertig!"
    echo "💾 Gespeichert als: $OUTPUT_FILE"
    echo ""
    echo "📝 Inhalt:"
    echo "=========================================="
    cat "$OUTPUT_FILE"
    echo "=========================================="
else
    echo "❌ Fehler bei der Transkription"
    exit 1
fi
