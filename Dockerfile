# Funding Finder - Production image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App and static assets
COPY app.py engine.py load_batches.py questionnaire.py schema.sql ./
COPY FUNDING_FINDER_FUN.html ./
COPY SAMPLE_FUNDING_REPORT.html ./
COPY start.sh ./
# All batch data for search (batch_11..35+, BATCH_2..10, FIRST_100 → 3,500 sources)
COPY batch_*.json ./
COPY BATCH_*_SOURCES.json ./
COPY FIRST_100_SOURCES.json ./

# Create data dir and PRE-BUILD the database at image build time
# This way the API responds instantly with all 3,500 sources - no loading on first request
RUN mkdir -p /app/data && chmod +x start.sh && \
    python3 -c "
import sqlite3
from pathlib import Path
db = '/app/data/funding_finder.db'
schema = Path('/app/schema.sql')
if schema.exists():
    conn = sqlite3.connect(db)
    conn.executescript(schema.read_text())
    conn.commit()
    conn.close()
" && \
    python3 -c "
from load_batches import load_all_batches
n = load_all_batches('/app/data/funding_finder.db')
print(f'Pre-loaded {n} funding sources into image')
"

ENV PORT=5000
EXPOSE 5000

# 1 worker = faster startup for Railway healthcheck; PORT from env
CMD ["./start.sh"]
