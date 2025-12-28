FROM python:3.11-slim

LABEL maintainer="AegisX Platform"
LABEL description="Thai DRG Grouper API"

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e .[api]

# Copy data
COPY data/ ./data/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["thai-drg-grouper", "serve", "--port", "8000", "--path", "./data/versions"]
