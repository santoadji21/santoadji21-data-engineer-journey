FROM python:3.11-slim

WORKDIR /app/dbt

# Install git (required for dbt deps sometimes)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We don't copy the project files here because we mount them in docker-compose
# This allows for local development
CMD ["tail", "-f", "/dev/null"]
