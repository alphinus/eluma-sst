#!/usr/bin/env python3
"""
Eluma STT - Local Speech-to-Text powered by whisper.cpp
Single server serving both the frontend and transcription API.
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os
import tempfile
import traceback

app = Flask(__name__)
CORS(app)

WHISPER_DIR = "/Users/developer/whisper.cpp"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Eluma STT - Speech to Text</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}

:root{
  --bg:#0f172a;
  --card:#141e33;
  --glass:rgba(255,255,255,0.02);
  --border:rgba(255,255,255,0.06);
  --cyan:#4fd1c5;
  --cyan-dim:rgba(79,209,197,0.15);
  --cyan-glow:rgba(79,209,197,0.3);
  --text:#e2e8f0;
  --text-dim:#64748b;
  --red:#ef4444;
  --amber:#f59e0b;
  --green:#22c55e;
}

body{
  font-family:system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  padding:24px 16px;
  overflow-x:hidden;
}

.logo{
  margin-bottom:8px;
  opacity:0;
  animation:fadeDown .6s cubic-bezier(.34,1.56,.64,1) forwards;
}
.logo svg{max-width:220px;height:auto}

.app-title{
  font-size:28px;
  font-weight:200;
  letter-spacing:4px;
  color:var(--text);
  margin-bottom:4px;
  opacity:0;
  animation:fadeDown .6s .1s cubic-bezier(.34,1.56,.64,1) forwards;
}
.app-subtitle{
  font-size:13px;
  font-weight:300;
  color:var(--text-dim);
  letter-spacing:2px;
  margin-bottom:32px;
  opacity:0;
  animation:fadeDown .6s .2s cubic-bezier(.34,1.56,.64,1) forwards;
}

.card{
  background:var(--glass);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border:1px solid var(--border);
  border-radius:16px;
  padding:32px;
  width:100%;
  max-width:520px;
  opacity:0;
  animation:fadeUp .6s .3s cubic-bezier(.34,1.56,.64,1) forwards;
}

/* Tabs */
.tabs{
  display:flex;
  gap:4px;
  background:rgba(255,255,255,0.03);
  border-radius:10px;
  padding:4px;
  margin-bottom:28px;
}
.tab{
  flex:1;
  padding:10px 16px;
  border:none;
  background:transparent;
  color:var(--text-dim);
  font-size:14px;
  font-weight:400;
  cursor:pointer;
  border-radius:8px;
  transition:all .25s ease;
  letter-spacing:.5px;
}
.tab:hover{color:var(--text)}
.tab.active{
  background:var(--cyan-dim);
  color:var(--cyan);
  font-weight:500;
}

/* Language */
.lang-row{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  margin-bottom:24px;
}
.lang-label{
  font-size:12px;
  color:var(--text-dim);
  letter-spacing:1px;
  text-transform:uppercase;
}
.lang-select{
  background:rgba(255,255,255,0.04);
  border:1px solid var(--border);
  color:var(--text);
  padding:8px 14px;
  border-radius:8px;
  font-size:14px;
  cursor:pointer;
  outline:none;
  transition:border-color .2s;
}
.lang-select:focus{border-color:var(--cyan)}
.lang-select option{background:var(--card);color:var(--text)}

/* Record section */
.record-section{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:16px;
}
.mic-btn{
  width:100px;
  height:100px;
  border-radius:50%;
  border:2px solid var(--cyan);
  background:var(--cyan-dim);
  color:var(--cyan);
  font-size:36px;
  cursor:pointer;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
}
.mic-btn:hover{
  transform:translateY(-3px);
  box-shadow:0 8px 32px var(--cyan-glow);
  background:rgba(79,209,197,0.25);
}
.mic-btn.recording{
  border-color:var(--red);
  background:rgba(239,68,68,0.15);
  color:var(--red);
  animation:pulse 1.5s ease-in-out infinite;
}
.mic-btn.recording:hover{
  box-shadow:0 8px 32px rgba(239,68,68,0.3);
}

/* Upload section */
.upload-section{display:none}
.upload-section.active{display:block}
.record-section-wrap{display:block}
.record-section-wrap.hidden{display:none}

.drop-zone{
  border:2px dashed var(--border);
  border-radius:12px;
  padding:40px 24px;
  text-align:center;
  cursor:pointer;
  transition:all .3s ease;
}
.drop-zone:hover,.drop-zone.dragover{
  border-color:var(--cyan);
  background:var(--cyan-dim);
}
.drop-zone-icon{
  font-size:40px;
  margin-bottom:12px;
  opacity:.6;
}
.drop-zone-text{
  font-size:14px;
  color:var(--text-dim);
  margin-bottom:8px;
}
.drop-zone-hint{
  font-size:12px;
  color:var(--text-dim);
  opacity:.6;
}
.browse-btn{
  display:inline-block;
  margin-top:12px;
  padding:8px 20px;
  background:var(--cyan-dim);
  color:var(--cyan);
  border:1px solid rgba(79,209,197,0.2);
  border-radius:8px;
  font-size:13px;
  cursor:pointer;
  transition:all .2s;
}
.browse-btn:hover{
  background:rgba(79,209,197,0.25);
  transform:translateY(-1px);
}
.file-info{
  margin-top:12px;
  padding:10px 14px;
  background:rgba(255,255,255,0.03);
  border-radius:8px;
  font-size:13px;
  color:var(--text-dim);
  display:none;
  align-items:center;
  gap:8px;
}
.file-info.show{display:flex}
.file-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.file-remove{
  cursor:pointer;
  color:var(--red);
  opacity:.7;
  font-size:16px;
  transition:opacity .2s;
}
.file-remove:hover{opacity:1}
.upload-btn{
  width:100%;
  margin-top:16px;
  padding:12px;
  background:var(--cyan);
  color:var(--bg);
  border:none;
  border-radius:10px;
  font-size:15px;
  font-weight:600;
  cursor:pointer;
  transition:all .2s;
  display:none;
}
.upload-btn:hover{
  transform:translateY(-1px);
  box-shadow:0 4px 20px var(--cyan-glow);
}
.upload-btn:disabled{
  opacity:.5;
  cursor:not-allowed;
  transform:none;
  box-shadow:none;
}
.upload-btn.show{display:block}

/* Status */
.status{
  text-align:center;
  margin-top:20px;
  font-size:14px;
  color:var(--text-dim);
  min-height:22px;
  transition:color .2s;
}
.status.recording{color:var(--red);font-weight:500}
.status.processing{color:var(--amber);font-weight:500}
.status.done{color:var(--green)}

/* Result */
.result{
  margin-top:20px;
  background:rgba(255,255,255,0.03);
  border:1px solid var(--border);
  border-radius:12px;
  padding:20px;
  display:none;
  animation:fadeUp .4s cubic-bezier(.34,1.56,.64,1);
}
.result.show{display:block}
.result-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:12px;
}
.result-label{
  font-size:12px;
  color:var(--cyan);
  letter-spacing:1px;
  text-transform:uppercase;
  font-weight:500;
}
.copy-btn{
  padding:6px 14px;
  background:rgba(255,255,255,0.04);
  border:1px solid var(--border);
  color:var(--text-dim);
  border-radius:6px;
  font-size:12px;
  cursor:pointer;
  transition:all .2s;
}
.copy-btn:hover{
  border-color:var(--cyan);
  color:var(--cyan);
}
.result-text{
  font-size:15px;
  line-height:1.7;
  color:var(--text);
  white-space:pre-wrap;
  word-break:break-word;
}

/* Toast */
.toast{
  position:fixed;
  bottom:24px;
  left:50%;
  transform:translateX(-50%) translateY(80px);
  background:var(--card);
  border:1px solid var(--border);
  color:var(--text);
  padding:12px 24px;
  border-radius:10px;
  font-size:14px;
  pointer-events:none;
  opacity:0;
  transition:all .3s cubic-bezier(.34,1.56,.64,1);
  z-index:100;
}
.toast.show{
  opacity:1;
  transform:translateX(-50%) translateY(0);
}

/* Footer */
.footer{
  margin-top:32px;
  font-size:12px;
  color:var(--text-dim);
  letter-spacing:1px;
  opacity:.5;
  text-align:center;
  opacity:0;
  animation:fadeUp .6s .5s ease forwards;
}

/* Animations */
@keyframes fadeDown{
  from{opacity:0;transform:translateY(-12px)}
  to{opacity:1;transform:translateY(0)}
}
@keyframes fadeUp{
  from{opacity:0;transform:translateY(12px)}
  to{opacity:1;transform:translateY(0)}
}
@keyframes pulse{
  0%,100%{transform:scale(1)}
  50%{transform:scale(1.06)}
}
@keyframes spin{
  to{transform:rotate(360deg)}
}

.spinner{
  display:inline-block;
  width:16px;
  height:16px;
  border:2px solid var(--border);
  border-top-color:var(--cyan);
  border-radius:50%;
  animation:spin .8s linear infinite;
  vertical-align:middle;
  margin-right:6px;
}

/* Responsive */
@media(max-width:560px){
  .card{padding:20px}
  .app-title{font-size:22px}
  .mic-btn{width:80px;height:80px;font-size:28px}
}
</style>
</head>
<body>

<div class="logo">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="40 60 120 120" width="100" height="100">
    <defs>
      <linearGradient id="ag" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#818cf8"/>
        <stop offset="50%" style="stop-color:#a5b4fc"/>
        <stop offset="100%" style="stop-color:#c7d2fe"/>
      </linearGradient>
      <linearGradient id="ig" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#818cf8"/>
        <stop offset="100%" style="stop-color:#c7d2fe"/>
      </linearGradient>
      <radialGradient id="gg" cx="50%" cy="50%" r="50%">
        <stop offset="0%" style="stop-color:#6366f1;stop-opacity:0.25"/>
        <stop offset="100%" style="stop-color:#6366f1;stop-opacity:0"/>
      </radialGradient>
      <filter id="sg"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#818cf8" flood-opacity="0.3"/></filter>
    </defs>
    <circle cx="100" cy="120" r="85" fill="url(#gg)"/>
    <g transform="translate(100,120)" filter="url(#sg)">
      <polygon points="0,-52 45,-26 45,26 0,52 -45,26 -45,-26" fill="none" stroke="url(#ig)" stroke-width="2" opacity="0.5"/>
      <rect x="-20" y="-28" width="32" height="5" rx="2.5" fill="url(#ag)" opacity="0.9"/>
      <rect x="16" y="-28" width="12" height="5" rx="2.5" fill="url(#ag)" opacity="0.5"/>
      <rect x="-20" y="-2.5" width="36" height="5" rx="2.5" fill="url(#ig)"/>
      <rect x="20" y="-2.5" width="8" height="5" rx="2.5" fill="url(#ig)" opacity="0.4"/>
      <rect x="-20" y="23" width="32" height="5" rx="2.5" fill="url(#ag)" opacity="0.9"/>
      <rect x="16" y="23" width="12" height="5" rx="2.5" fill="url(#ag)" opacity="0.5"/>
      <rect x="-22" y="-30" width="5" height="58" rx="2.5" fill="url(#ig)"/>
      <circle cx="34" cy="-26" r="2" fill="#a5b4fc" opacity="0.7"/>
      <circle cx="38" cy="0" r="1.5" fill="#818cf8" opacity="0.5"/>
      <circle cx="34" cy="25" r="2" fill="#a5b4fc" opacity="0.7"/>
      <circle cx="0" cy="-52" r="3" fill="#818cf8"/>
      <circle cx="45" cy="-26" r="2.5" fill="#a5b4fc"/>
      <circle cx="45" cy="26" r="2.5" fill="#a5b4fc"/>
      <circle cx="0" cy="52" r="3" fill="#818cf8"/>
      <circle cx="-45" cy="26" r="2.5" fill="#a5b4fc"/>
      <circle cx="-45" cy="-26" r="2.5" fill="#a5b4fc"/>
    </g>
  </svg>
</div>

<div class="app-title">SPEECH TO TEXT</div>
<div class="app-subtitle">100% lokal &middot; whisper.cpp</div>

<div class="card">
  <!-- Tabs -->
  <div class="tabs">
    <button class="tab active" data-tab="record">Live Aufnahme</button>
    <button class="tab" data-tab="upload">Datei hochladen</button>
  </div>

  <!-- Language -->
  <div class="lang-row">
    <span class="lang-label">Sprache</span>
    <select class="lang-select" id="language">
      <option value="de">Deutsch</option>
      <option value="en">English</option>
      <option value="fr">Francais</option>
      <option value="es">Espanol</option>
      <option value="it">Italiano</option>
    </select>
  </div>

  <!-- Record Tab -->
  <div class="record-section-wrap" id="recordTab">
    <div class="record-section">
      <button class="mic-btn" id="micBtn">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
          <line x1="12" y1="19" x2="12" y2="23"/>
          <line x1="8" y1="23" x2="16" y2="23"/>
        </svg>
      </button>
    </div>
  </div>

  <!-- Upload Tab -->
  <div class="upload-section" id="uploadTab">
    <div class="drop-zone" id="dropZone">
      <div class="drop-zone-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--text-dim)">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </div>
      <div class="drop-zone-text">Datei hierher ziehen</div>
      <div class="drop-zone-hint">.ogg .wav .mp3 .mp4 .m4a .webm</div>
      <button class="browse-btn" id="browseBtn">Datei auswaehlen</button>
    </div>
    <input type="file" id="fileInput" accept=".ogg,.wav,.mp3,.mp4,.m4a,.webm,audio/*" style="display:none">
    <div class="file-info" id="fileInfo">
      <span class="file-name" id="fileName"></span>
      <span class="file-remove" id="fileRemove">&times;</span>
    </div>
    <button class="upload-btn" id="uploadBtn">Transkribieren</button>
  </div>

  <!-- Status -->
  <div class="status" id="status">Bereit</div>

  <!-- Result -->
  <div class="result" id="result">
    <div class="result-header">
      <span class="result-label">Transkription</span>
      <button class="copy-btn" id="copyBtn">Kopieren</button>
    </div>
    <div class="result-text" id="resultText"></div>
  </div>
</div>

<div class="footer">100% Lokal &middot; Kostenlos &middot; whisper.cpp</div>

<div class="toast" id="toast"></div>

<script>
const $ = s => document.getElementById(s);
const micBtn = $('micBtn');
const status = $('status');
const result = $('result');
const resultText = $('resultText');
const langSelect = $('language');
const dropZone = $('dropZone');
const fileInput = $('fileInput');
const fileInfo = $('fileInfo');
const fileName = $('fileName');
const fileRemove = $('fileRemove');
const uploadBtn = $('uploadBtn');
const copyBtn = $('copyBtn');
const toast = $('toast');
const recordTab = $('recordTab');
const uploadTab = $('uploadTab');

let mediaRecorder = null;
let audioChunks = [];
let selectedFile = null;

// Tabs
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const target = tab.dataset.tab;
    if (target === 'record') {
      recordTab.classList.remove('hidden');
      uploadTab.classList.remove('active');
    } else {
      recordTab.classList.add('hidden');
      uploadTab.classList.add('active');
    }
  });
});

// Microphone recording
micBtn.addEventListener('click', async () => {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        await transcribe(blob, 'recording.webm');
      };
      mediaRecorder.start();
      micBtn.classList.add('recording');
      setStatus('Aufnahme laeuft...', 'recording');
      result.classList.remove('show');
    } catch (e) {
      setStatus('Mikrofon-Zugriff verweigert', '');
    }
  } else {
    mediaRecorder.stop();
    micBtn.classList.remove('recording');
    setStatus('<span class="spinner"></span> Transkribiere...', 'processing');
  }
});

// File upload - drag & drop
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files.length) selectUploadFile(e.dataTransfer.files[0]);
});
dropZone.addEventListener('click', e => {
  if (e.target.id !== 'browseBtn') fileInput.click();
});
document.getElementById('browseBtn').addEventListener('click', e => {
  e.stopPropagation();
  fileInput.click();
});
fileInput.addEventListener('change', () => {
  if (fileInput.files.length) selectUploadFile(fileInput.files[0]);
});
fileRemove.addEventListener('click', () => clearFile());

function selectUploadFile(file) {
  const ext = file.name.split('.').pop().toLowerCase();
  const allowed = ['ogg','wav','mp3','mp4','m4a','webm'];
  if (!allowed.includes(ext)) {
    showToast('Format nicht unterstuetzt');
    return;
  }
  selectedFile = file;
  fileName.textContent = file.name;
  fileInfo.classList.add('show');
  uploadBtn.classList.add('show');
}

function clearFile() {
  selectedFile = null;
  fileInput.value = '';
  fileInfo.classList.remove('show');
  uploadBtn.classList.remove('show');
}

uploadBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  uploadBtn.disabled = true;
  setStatus('<span class="spinner"></span> Transkribiere...', 'processing');
  result.classList.remove('show');
  await transcribe(selectedFile, selectedFile.name);
  uploadBtn.disabled = false;
});

// Transcription
async function transcribe(blob, filename) {
  const fd = new FormData();
  fd.append('audio', blob, filename);
  fd.append('language', langSelect.value);
  try {
    const res = await fetch('/transcribe', { method: 'POST', body: fd });
    const data = await res.json();
    if (data.success) {
      resultText.textContent = data.transcription;
      result.classList.add('show');
      setStatus('Fertig', 'done');
    } else {
      setStatus('Fehler: ' + data.error, '');
    }
  } catch (e) {
    setStatus('Server nicht erreichbar', '');
  }
}

// Copy
copyBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(resultText.textContent).then(() => {
    showToast('Kopiert!');
  });
});

// Helpers
function setStatus(html, cls) {
  status.innerHTML = html;
  status.className = 'status' + (cls ? ' ' + cls : '');
}

function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2000);
}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return Response(HTML_TEMPLATE, mimetype='text/html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    temp_files = []
    try:
        audio_file = request.files.get('audio')
        language = request.form.get('language', 'de')

        if not audio_file:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400

        # Determine input extension from filename
        orig_name = audio_file.filename or 'audio.webm'
        ext = os.path.splitext(orig_name)[1] or '.webm'
        print(f"\n🎙️  Audio empfangen: {orig_name} (Sprache: {language})")

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            audio_file.save(tmp.name)
            input_path = tmp.name
            temp_files.append(input_path)

        # Convert to 16kHz mono WAV
        wav_path = input_path + '.wav'
        temp_files.append(wav_path)

        try:
            subprocess.run([
                'ffmpeg', '-i', input_path,
                '-ar', '16000', '-ac', '1',
                '-c:a', 'pcm_s16le', '-y',
                wav_path
            ], check=True, capture_output=True, timeout=30)
            print("✅ Konvertiert zu WAV")
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            import shutil
            shutil.copy(input_path, wav_path)
            print(f"⚠️  ffmpeg nicht verfuegbar, nutze Originaldatei")

        # Model selection: EN -> small.en, others -> medium, fallbacks
        if language == 'en':
            model = f"{WHISPER_DIR}/models/ggml-small.en.bin"
        else:
            model = f"{WHISPER_DIR}/models/ggml-medium.bin"

        if not os.path.exists(model):
            model = f"{WHISPER_DIR}/models/ggml-small.bin"
        if not os.path.exists(model):
            model = f"{WHISPER_DIR}/models/ggml-base.bin"
        if not os.path.exists(model):
            return jsonify({'success': False, 'error': 'Kein Whisper-Modell gefunden'}), 500

        print(f"🧠 Modell: {os.path.basename(model)}")

        output_base = wav_path.replace('.wav', '')
        output_file = f"{output_base}.txt"
        temp_files.append(output_file)

        cmd = [
            f"{WHISPER_DIR}/build/bin/whisper-cli",
            "-m", model,
            "-f", wav_path,
            "-l", language,
            "-ng", "-otxt",
            "-of", output_base,
            "-np", "-nt"
        ]

        print("🚀 Transkription laeuft...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"❌ Fehler: {result.stderr}")
            return jsonify({
                'success': False,
                'error': f'Transkription fehlgeschlagen: {result.stderr[:200]}'
            }), 500

        transcription = ""
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                transcription = f.read().strip()
            print(f"✅ Ergebnis: {transcription[:100]}...")
        else:
            return jsonify({'success': False, 'error': 'Keine Ausgabedatei'}), 500

        if transcription:
            return jsonify({'success': True, 'transcription': transcription})
        else:
            return jsonify({'success': False, 'error': 'Leere Transkription'}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Timeout'}), 500
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("=" * 44)
    print("  ELUMA STT - Local Speech to Text")
    print("=" * 44)
    print(f"  Server:  http://localhost:5001")
    print(f"  Engine:  whisper.cpp")
    print("=" * 44)
    print("")
    app.run(host='0.0.0.0', port=5001, debug=False)
