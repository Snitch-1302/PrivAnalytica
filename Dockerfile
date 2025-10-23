# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ backend/

# Copy the frontend code
COPY frontend/ frontend/

# Copy the start script
COPY start_server.py .

# Create directory for reports and logs
RUN mkdir -p backend/reports

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "backend/main.py"]