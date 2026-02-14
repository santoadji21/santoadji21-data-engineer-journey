.PHONY: up down logs clean help install run-legacy run-modern run-budget

# Default target
help:
	@echo "Hotel Real-Time Pipeline"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Infrastructure:"
	@echo "  up          Start Redpanda (Kafka) & Console"
	@echo "  down        Stop Redpanda"
	@echo "  logs        View Redpanda logs"
	@echo "  clean       Remove containers and data volumes"
	@echo ""
	@echo "Python:"
	@echo "  install     Install Python dependencies"
	@echo "  run-legacy  Start Legacy PMS Producer"
	@echo "  run-modern  Start Modern PMS Producer"
	@echo "  run-budget  Start Budget PMS Producer"

up:
	docker-compose up -d
	@echo ""
	@echo "Redpanda Console: http://localhost:8080"
	@echo "Kafka Broker:     localhost:9092"

build:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	@echo "Cleaned up containers and volumes"

install:
	pip install -r requirements.txt

run-legacy:
	python producer/pms_legacy.py

run-modern:
	python producer/pms_modern.py

run-budget:
	python producer/pms_budget.py
