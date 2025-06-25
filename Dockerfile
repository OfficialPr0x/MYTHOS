FROM python:3.10-slim

WORKDIR /titan

COPY . /titan

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    curl \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with optimized builds
RUN pip install --no-cache-dir \
    torch==2.0.1 \
    transformers==4.30.2 \
    numpy==1.24.3 \
    scipy==1.10.1 \
    faiss-cpu==1.7.4 \
    websockets==11.0.3 \
    cryptography==41.0.0 \
    grpcio==1.54.2 \
    scikit-learn==1.2.2 \
    pandas==2.0.2 \
    networkx==3.1 \
    matplotlib==3.7.1 \
    nltk==3.8.1 \
    sentence-transformers==2.2.2 \
    statsmodels==0.14.0 \
    psutil==5.9.5

# Create vault directory
RUN mkdir -p /vault && chmod 777 /vault

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TITAN_HOME=/titan
ENV VAULT_PATH=/vault

# Expose the WebSocket port
EXPOSE 8888

# Set default command
CMD ["python", "main.py"]
