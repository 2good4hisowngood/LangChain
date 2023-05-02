# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

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
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ARG SERPAPI_API_KEY
ENV SERPAPI_API_KEY=$SERPAPI_API_KEY

# Run Gunicorn to serve the Flask app and display meaningful error messages
CMD gunicorn -b 0.0.0.0:5000 app:app 2>&1 \
    || { echo "Error: Failed to start Gunicorn server"; exit 1; }
