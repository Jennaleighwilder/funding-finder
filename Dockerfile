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

# Create data dir for SQLite (writable at runtime)
RUN mkdir -p /app/data

ENV PORT=5000
EXPOSE 5000

# Use gunicorn; PORT is set by Railway/Render etc.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 app:app"]
