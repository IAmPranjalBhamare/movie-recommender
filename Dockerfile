# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and data
COPY app.py .
COPY tmdb_5000_movies.csv .
COPY tmdb_5000_credits.csv .
COPY generate_models.py .
COPY gunicorn_config.py .

# Generate model files at build time
RUN python generate_models.py

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run the application with optimized settings for limited memory
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
