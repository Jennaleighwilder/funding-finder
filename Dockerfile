# Funding Finder - Production image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App and static assets
COPY app.py engine.py questionnaire.py schema.sql ./
COPY FUNDING_FINDER_FUN.html ./
COPY SAMPLE_FUNDING_REPORT.html ./
COPY start.sh ./

# Create data dir for SQLite (writable at runtime)
RUN mkdir -p /app/data && chmod +x start.sh

ENV PORT=5000
EXPOSE 5000

# 1 worker = faster startup for Railway healthcheck; PORT from env
CMD ["./start.sh"]
