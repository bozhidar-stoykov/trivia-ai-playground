#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL to be fully ready
until pg_isready -h postgres -p 5432 -U postgres; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"
echo "Starting data ingestion..."

# Run the ingestion script
python ingestion_script.py

echo "Data ingestion completed!"

# Keep container running for inspection (optional - comment out if not needed)
# tail -f /dev/null
