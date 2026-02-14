.PHONY: up down build generate run test shell clean help

# Default target
help:
	@echo "Hotel dbt Transformation Project"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up        Start the dbt container"
	@echo "  down      Stop the dbt container"
	@echo "  build     Rebuild the dbt container"
	@echo "  generate  Generate test data (Parquet)"
	@echo "  run       Run dbt models"
	@echo "  test      Run dbt tests"
	@echo "  query     Query the DuckDB results"
	@echo "  shell     Open bash shell in container"
	@echo "  clean     Remove containers and volumes"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up --build -d

generate:
	docker-compose exec dbt python generate_data.py

run:
	docker-compose exec dbt dbt run

test:
	docker-compose exec dbt dbt test

query:
	docker-compose exec dbt python query_results.py

shell:
	docker-compose exec dbt bash

clean:
	docker-compose down -v
