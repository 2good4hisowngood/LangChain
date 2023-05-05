# Use the official Python 3.8 slim image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install build-essential to allow for the installation of Python packages with C extensions for chromadb
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python packages specified in requirements.txt and display meaningful error messages
RUN pip install --no-cache-dir -r requirements.txt 2>&1 \
    || { echo "Error: Failed to install packages from requirements.txt"; exit 1; }

# Copy all remaining files from the host machine to the working directory
COPY . .

# Copy static and templates folders from the host machine to their respective directories in the image
COPY static/ /app/static/
COPY templates/ /app/templates/

# Expose port 5000 for external access
EXPOSE 5000

# Set environment variables for API keys
ARG OPENAI_API_KEY
ARG SERPAPI_API_KEY
ARG PINECONE_API_KEY 
ARG PINECONE_ENV 

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV SERPAPI_API_KEY=${SERPAPI_API_KEY}
ENV PINECONE_API_KEY=${PINECONE_API_KEY}
ENV PINECONE_ENV =${PINECONE_ENV}

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]