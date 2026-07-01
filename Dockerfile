FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application codebase
COPY . .

# Expose Cloud Run default port
EXPOSE 8080

# Run production WSGI server with thread support for Server-Sent Events (SSE) streaming
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 --timeout 0 dashboard.app:app"]
