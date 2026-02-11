# 🎙️ KOSTENLOSE Whisper Transkription - FERTIG!

## ✅ Was ist installiert:

- **whisper.cpp** - Kompiliert und einsatzbereit
- **Models**: tiny.en (~75MB), base (~150MB)
- **Skript**: `/Users/developer/whisper-transcribe.sh`

---

## 🚀 VERWENDUNG

### Einfache Nutzung:
```bash
./whisper-transcribe.sh deine_audio.mp3 de
```

### Beispiele:
```bash
# Deutsche Audio transkribieren
./whisper-transcribe.sh podcast.mp3 de

# Englische Audio transkribieren
./whisper-transcribe.sh interview.wav en

# Französisch
./whisper-transcribe.sh video.m4a fr

# Auto-Erkennung (manchmal ungenau)
./whisper-transcribe.sh audio.mp3 auto
```

---

## 📊 MODELLE

Du kannst zwischen verschiedenen Modellen wählen:

| Modell | Größe | Geschwindigkeit | Genauigkeit |
|--------|-------|-----------------|-------------|
| tiny.en | 75MB | ⚡⚡⚡⚡ Sehr schnell | ⭐⭐ Basis |
| base | 150MB | ⚡⚡⚡ Schnell | ⭐⭐⭐ Gut (Standard) |
| small | 500MB | ⚡⚡ Mittel | ⭐⭐⭐⭐ Sehr gut |
| medium | 1.5GB | ⚡ Langsam | ⭐⭐⭐⭐⭐ Exzellent |
| large-v3 | 3GB | 🐌 Sehr langsam | ⭐⭐⭐⭐⭐ Beste |

### Modell wechseln:
```bash
MODEL=small ./whisper-transcribe.sh audio.mp3 de
MODEL=medium ./whisper-transcribe.sh audio.mp3 en
```

### Modell herunterladen:
```bash
cd /Users/developer/whisper.cpp
bash ./models/download-ggml-model.sh small
bash ./models/download-ggml-model.sh medium
bash ./models/download-ggml-model.sh large-v3
```

---

## 🌍 UNTERSTÜTZTE SPRACHEN

**Deutsch**: `de`
**Englisch**: `en`
**Französisch**: `fr`
**Spanisch**: `es`
**Italienisch**: `it`
**Portugiesisch**: `pt`
**Niederländisch**: `nl`
**Russisch**: `ru`
**Japanisch**: `ja`
**Chinesisch**: `zh`
**Koreanisch**: `ko`
**Arabisch**: `ar`
**Türkisch**: `tr`
**Polnisch**: `pl`
**Ukrainisch**: `uk`

...und 84 weitere Sprachen!

---

## 📁 UNTERSTÜTZTE FORMATE

✅ MP3, WAV, M4A, AAC
✅ FLAC, OGG, OPUS
✅ MP4 (Audio wird extrahiert)
✅ WebM, MKV

---

## 💡 TIPPS FÜR BESTE ERGEBNISSE

1. **Wähle das richtige Modell:**
   - Für schnelle Tests: `tiny` oder `base`
   - Für Produktion: `small` oder `medium`
   - Für beste Qualität: `large-v3`

2. **Gib die Sprache an:**
   - Auto-Erkennung ist manchmal ungenau
   - Besser: Sprache explizit angeben

3. **Audio-Qualität:**
   - Klarere Aufnahmen = bessere Ergebnisse
   - Wenig Hintergrundgeräusche ideal

4. **Batch-Verarbeitung:**
   ```bash
   for file in *.mp3; do
       ./whisper-transcribe.sh "$file" de
   done
   ```

---

## 🆓 KOMPLETT KOSTENLOS!

- ✅ Keine API-Kosten
- ✅ Unbegrenzte Nutzung
- ✅ Funktioniert offline
- ✅ Deine Daten bleiben lokal
- ✅ Open Source

---

## 🔧 ERWEITERT

### Direkter Aufruf (ohne Skript):
```bash
cd /Users/developer/whisper.cpp
./build/bin/whisper-cli -m models/ggml-base.bin -f audio.mp3 -l de -otxt
```

### Mit Zeitstempeln (SRT für Untertitel):
```bash
./build/bin/whisper-cli -m models/ggml-base.bin -f video.mp4 -l de -osrt
```

### JSON Output:
```bash
./build/bin/whisper-cli -m models/ggml-base.bin -f audio.mp3 -l de -oj
```

---

## 📖 HILFE

```bash
# Hilfe anzeigen
./whisper-transcribe.sh

# Whisper-CLI Hilfe
./build/bin/whisper-cli --help
```

---

## 🎯 SCHNELLSTART

```bash
# 1. Transkribiere eine deutsche Audiodatei
./whisper-transcribe.sh meine_aufnahme.mp3 de

# 2. Ergebnis wird gespeichert als: meine_aufnahme.txt

# 3. Fertig! 🎉
```

---

**Viel Erfolg mit deiner Transkription!** 🚀
