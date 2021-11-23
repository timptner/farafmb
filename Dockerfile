# Use python as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . /app
