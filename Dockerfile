# Use an official Python 3.11 runtime as a parent image
FROM python:3.11-slim-buster # <-- CHANGE THIS LINE to a stable version

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (as needed for your OCR and other libraries)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-tam \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    pkg-config \
    # Add any other system dependencies your specific OCR libraries might need
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (including pandas)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your FastAPI application listens on
EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
