# Dockerfile
FROM python:3.10-slim

# Prevent python writing .pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app

# Create tmp for model caching (recommended in Spaces docs)
RUN mkdir -p /tmp/models
ENV TRANSFORMERS_CACHE=/tmp/models
ENV HF_HOME=/tmp/home

# Expose port used by Spaces (default 7860)
ENV PORT=7860
EXPOSE 7860

# Use gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--workers", "1", "--threads", "2", "--timeout", "300"]
