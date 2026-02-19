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
COPY init_db.py ./
RUN mkdir -p /app/data && chmod +x start.sh && python3 init_db.py

ENV PORT=5000
EXPOSE 5000

# 1 worker = faster startup for Railway healthcheck; PORT from env
CMD ["./start.sh"]
