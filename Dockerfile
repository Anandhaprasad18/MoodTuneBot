# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/tmp/models \
    PORT=7860

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port expected by Hugging Face
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
