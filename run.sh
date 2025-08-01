#!/bin/bash
set -e

FLASK_PORT=5000

echo "🚀 Launching Flask server on http://localhost:$FLASK_PORT"

# Run Flask in foreground to see errors directly
python3 app/app.py
