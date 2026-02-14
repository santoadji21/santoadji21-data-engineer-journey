.PHONY: up down build logs clean help

help:
	@echo "Hotel Orchestrator (Dagster)"
	@echo "Usage: make [target]"
	@echo ""
	@echo "  up      Start Dagster"
	@echo "  down    Stop Dagster"
	@echo "  build   Rebuild Dagster"
	@echo "  logs    View logs"
	@echo "  clean   Remove containers"

up:
	docker-compose up -d
	@echo "Dagster UI: http://localhost:3000"

down:
	docker-compose down

build:
	docker-compose up --build -d

logs:
	docker-compose logs -f

clean:
	docker-compose down -v

rebuild:
	docker-compose down
	docker-compose up --build -d

restart:
	docker-compose restart
