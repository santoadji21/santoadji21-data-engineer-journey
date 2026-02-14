.PHONY: build up down restart logs shell clean help

# Default target
help:
	@echo "Python Basic - Jupyter Environment"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build    Build Docker image"
	@echo "  up       Start Jupyter container"
	@echo "  down     Stop Jupyter container"
	@echo "  restart  Restart Jupyter container"
	@echo "  logs     View container logs"
	@echo "  shell    Open bash shell in container"
	@echo "  clean    Remove container and image"
	@echo "  help     Show this help message"

# Build the Docker image
build:
	docker compose build

# Start the container
up:
	docker compose up -d
	@echo ""
	@echo "Jupyter is running at: http://localhost:8888"

# Stop the container
down:
	docker compose down

# Restart the container
restart: down up

# View logs
logs:
	docker compose logs -f

# Open shell in container
shell:
	docker compose exec jupyter bash

# Clean up everything
clean:
	docker compose down -v --rmi local
	@echo "Cleaned up containers and images"
