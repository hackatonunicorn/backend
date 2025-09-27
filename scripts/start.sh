#!/bin/bash

# Start script for Railway deployment
echo "Starting Unicorn Authentication API..."

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
