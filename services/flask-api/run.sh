#!/usr/bin/env bash
set -euo pipefail

# Activate venv relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/venv/bin/activate"

# Default port if not supplied
PORT="${PORT:-5000}"

echo "Starting Gunicorn on 0.0.0.0:${PORT}"
exec gunicorn --bind 0.0.0.0:${PORT} wsgi:application --workers 2 --timeout 60
