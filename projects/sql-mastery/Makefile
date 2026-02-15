.PHONY: up down build logs clean help

help:
	@echo "SQL Mastery Lab"
	@echo "Usage: make [target]"
	@echo ""
	@echo "  up      Start Jupyter, Postgres, PgAdmin"
	@echo "  down    Stop services"
	@echo "  build   Rebuild Jupyter image"
	@echo "  logs    View logs"
	@echo "  clean   Remove containers and volumes"

up:
	docker-compose up -d
	@echo ""
	@echo "Jupyter Lab: http://localhost:8888"
	@echo "PgAdmin:     http://localhost:5050 (admin@admin.com / password)"
	@echo "Postgres:    localhost:5432"

down:
	docker-compose down

build:
	docker-compose up --build -d

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
