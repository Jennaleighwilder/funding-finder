# Funding Finder - Production image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App and static assets - copy everything in one go to avoid glob issues
COPY . .

# Create data dir, make start executable
RUN mkdir -p /app/data && chmod +x start.sh

ENV PORT=5000
EXPOSE 5000

CMD ["./start.sh"]
