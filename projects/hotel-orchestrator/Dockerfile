FROM python:3.11-slim

# Install git (required for dbt deps) and bash
RUN apt-get update && apt-get install -y git bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set DAGSTER_HOME
ENV DAGSTER_HOME=/app/dagster_home
RUN mkdir -p $DAGSTER_HOME

COPY . .

# Default command to run the webserver
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
