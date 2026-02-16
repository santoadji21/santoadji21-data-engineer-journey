#!/bin/bash
set -e

# This script runs automatically on first Postgres startup.
# The default database (mastery_db) is already created via POSTGRES_DB env var.

create_db_if_not_exists() {
  local db=$1
  if psql -U "$POSTGRES_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$db'" | grep -q 1; then
    echo "Database '$db' already exists — skipping."
  else
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $db;"
    psql -U "$POSTGRES_USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $db TO $POSTGRES_USER;"
    echo "Database '$db' created."
  fi
}

create_db_if_not_exists "analytics_db"
create_db_if_not_exists "development_db"
