#!/bin/bash

echo ""
echo "============================================"
echo "  ELUMA STT - Local Speech to Text"
echo "============================================"
echo ""

# Start server in background
python3 /Users/developer/whisper-local-stt/browser-app/server.py &
SERVER_PID=$!

# Wait for server to be ready
echo "  Server startet..."
sleep 2

# Open browser
echo "  Browser oeffnet..."
open http://localhost:5001

echo ""
echo "  App laeuft: http://localhost:5001"
echo "  Beenden:    Ctrl+C"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '  Server beendet.'; kill $SERVER_PID 2>/dev/null; exit" INT
wait $SERVER_PID
