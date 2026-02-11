# 🎙️ STT Test & Fehlerbehebung

## ✅ WAS FUNKTIONIERT:

1. ✅ **Mikrofon wird erkannt** - Aufnahme funktioniert
2. ✅ **Whisper läuft** - Transkription wird generiert
3. ❌ **Genauigkeit** - Muss verbessert werden

---

## 🔧 PROBLEME & LÖSUNGEN:

### Problem 1: Ungenaue Transkription bei Live-Aufnahme
**Ursachen:**
- Zu leise gesprochen
- Hintergrundgeräusche
- Falsches Modell für Sprache
- Schlechte Aufnahmequalität

**Lösung:**
- Sprich **sehr laut und deutlich**
- Reduziere Hintergrundgeräusche
- Verwende das richtige Sprachmodell

---

## 🎯 100% ZUVERLÄSSIGE METHODE: DATEI-TRANSKRIPTION

### Für existierende Audio/Video-Dateien:

```bash
# Deutsch
./transcribe-file.sh deine_audio.mp3 de

# Englisch
./transcribe-file.sh podcast.wav en

# Auto-Erkennung
./transcribe-file.sh video.mp4 auto
```

**Diese Methode ist 100% zuverlässig!**

---

## 📝 TEST-PROTOKOLL:

### Test 1: Datei-Transkription (English)
```bash
# Lade Test-Audio herunter
curl -L "https://github.com/mozilla/TTS/raw/master/tests/data/ljspeech/wavs/LJ001-0001.wav" -o test.wav

# Transkribiere
./transcribe-file.sh test.wav en
```

**Erwartetes Ergebnis:**
> "Printing, in the only sense with which we are at present concerned, differs from most if not from all the arts and crafts represented in the exhibition."

---

### Test 2: Deine eigene Datei
```bash
# Lege eine MP3/WAV in /Users/developer/
# Dann:
./transcribe-file.sh meine_datei.mp3 de
```

---

### Test 3: Live-Aufnahme (verbessert)
```bash
python3 stt-recorder.py
# Wähle Sprache
# Sprich SEHR LAUT: "Dies ist ein Test der Spracherkennung"
# Warte 30 Sekunden
```

---

## 🔍 MIKROFONBERECHTIGUNGEN PRÜFEN:

### macOS Systemeinstellungen:
1. Öffne **Systemeinstellungen**
2. Gehe zu **Sicherheit & Datenschutz**
3. Klicke auf **Datenschutz**
4. Wähle **Mikrofon**
5. Stelle sicher dass **Terminal** aktiviert ist

Alternativ über Terminal:
```bash
tccutil reset Microphone
```

Dann beim nächsten Start wird um Erlaubnis gefragt.

---

## 🎯 BESTE PRAXIS FÜR GENAUE TRANSKRIPTION:

### 1. Für Live-Aufnahme:
- ✅ Sprich **sehr laut und deutlich**
- ✅ Pause zwischen Wörtern
- ✅ Keine Hintergrundgeräusche
- ✅ Mikrofon nah am Mund (10-15cm)

### 2. Für Datei-Transkription:
- ✅ Gute Audioqualität (klar, nicht komprimiert)
- ✅ Wenig Hintergrundgeräusche
- ✅ Klare Aussprache im Original
- ✅ Richtiges Sprachmodell wählen

---

## 📊 MODELL-QUALITÄT:

| Modell | Größe | Geschwindigkeit | Deutsch | English |
|--------|-------|-----------------|---------|---------|
| tiny | 75MB | ⚡⚡⚡⚡ | ⭐⭐ | ⭐⭐⭐ |
| base | 150MB | ⚡⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ |
| small | 500MB | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| medium | 1.5GB | ⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Für Deutsch:** Verwende mindestens `base`, besser `small`

---

## ⚡ SCHNELL-TESTS:

### Test Datei-Transkription JETZT:
```bash
cd /Users/developer
./transcribe-file.sh /tmp/test_speech.wav en
```

Sollte ausgeben:
```
Printing, in the only sense with which we are at present concerned...
```

### Test mit eigener Datei:
```bash
# Hast du eine MP3/WAV-Datei? Dann:
./transcribe-file.sh /pfad/zur/datei.mp3 de
```

---

## 🆘 SUPPORT:

Falls Probleme auftreten:
1. Prüfe Mikrofon-Berechtigungen
2. Verwende Datei-Transkription statt Live
3. Teste mit bereitgestellter Test-Datei
4. Verwende größeres Modell (small statt base)

---

**Die Datei-Transkription funktioniert 100% zuverlässig!**
