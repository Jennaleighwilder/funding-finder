#!/bin/sh
# Use PORT from environment (Railway, Render, etc.)
PORT="${PORT:-5000}"
exec gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 4 --timeout 120 app:app
