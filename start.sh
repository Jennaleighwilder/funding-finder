#!/bin/sh
# Use PORT from environment (Railway, Render, etc.)
PORT="${PORT:-5000}"

# Pre-load DB at startup so first API request is fast (3,500 sources)
echo "Initializing database..."
python3 -c "
import sqlite3
from pathlib import Path
db = '/app/data/funding_finder.db'
Path('/app/data').mkdir(exist_ok=True)
s = Path('/app/schema.sql')
if s.exists():
    c = sqlite3.connect(db)
    c.executescript(s.read_text())
    c.commit()
    c.close()
from load_batches import load_all_batches
n = load_all_batches(db)
print(f'Loaded {n} funding sources')
" 2>/dev/null || true

exec gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 4 --timeout 120 app:app
