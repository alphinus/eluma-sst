#!/bin/bash
# Zuverlässige Datei-Transkription
# Verwendung: ./transcribe-file.sh audio.mp3 [sprache]

if [ -z "$1" ]; then
    echo "❌ Keine Datei angegeben"
    echo ""
    echo "Verwendung:"
    echo "  ./transcribe-file.sh audio.mp3"
    echo "  ./transcribe-file.sh audio.wav de"
    echo "  ./transcribe-file.sh video.mp4 en"
    echo ""
    echo "Unterstützte Formate: mp3, wav, m4a, mp4, webm, flac, ogg"
    echo "Sprachen: de, en, fr, es, it, pt, nl, ru, ja, zh, ..."
    exit 1
fi

AUDIO_FILE="$1"
LANGUAGE="${2:-auto}"
WHISPER_DIR="/Users/developer/whisper.cpp"

# Prüfe ob Datei existiert
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ Datei nicht gefunden: $AUDIO_FILE"
    exit 1
fi

# Wähle Modell basierend auf Sprache
if [ "$LANGUAGE" = "en" ]; then
    MODEL="$WHISPER_DIR/models/ggml-small.en.bin"
else
    MODEL="$WHISPER_DIR/models/ggml-base.bin"
fi

# Fallback zu base wenn Model nicht existiert
if [ ! -f "$MODEL" ]; then
    MODEL="$WHISPER_DIR/models/ggml-base.bin"
fi

echo "🎙️  Transkribiere: $(basename "$AUDIO_FILE")"
echo "🌍 Sprache: $LANGUAGE"
echo "🧠 Modell: $(basename "$MODEL")"
echo ""
echo "⏳ Bitte warten..."
echo ""

# Output-Dateien
OUTPUT_BASE="${AUDIO_FILE%.*}_transcript"
OUTPUT_TXT="${OUTPUT_BASE}.txt"

# Führe Transkription aus
$WHISPER_DIR/build/bin/whisper-cli \
    -m "$MODEL" \
    -f "$AUDIO_FILE" \
    -l "$LANGUAGE" \
    -ng \
    -otxt \
    -of "$OUTPUT_BASE" \
    2>&1 | grep -E "processing|whisper_print_timings"

if [ -f "$OUTPUT_TXT" ]; then
    echo ""
    echo "✅ Transkription erfolgreich!"
    echo "💾 Gespeichert: $OUTPUT_TXT"
    echo ""
    echo "📝 TRANSKRIPTION:"
    echo "=========================================="
    cat "$OUTPUT_TXT"
    echo "=========================================="
else
    echo ""
    echo "❌ Transkription fehlgeschlagen"
    exit 1
fi
