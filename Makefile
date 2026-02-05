.PHONY: help setup install docker-up docker-down docker-logs phase1-generate phase1-analyze clean test

# Default target
help:
	@echo "🚀 Data Engineering Journey - Available Commands"
	@echo ""
	@echo "📦 Environment Setup:"
	@echo "  make setup          - Create virtual environment and install dependencies"
	@echo "  make install        - Install Python dependencies only"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo "  make docker-logs    - View Docker logs"
	@echo "  make docker-shell   - Open shell in container"
	@echo ""
	@echo "🏨 Phase 1 - Hotel Lifecycle:"
	@echo "  make phase1-generate - Generate sample hotel booking data"
	@echo "  make phase1-analyze  - Analyze bookings with DuckDB"
	@echo "  make phase1-full     - Generate + Analyze (complete pipeline)"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean          - Remove generated data and cache files"
	@echo "  make clean-all      - Remove everything including venv"

# Environment setup
setup:
	@echo "🔧 Setting up Python virtual environment..."
	cd environment && python3 -m venv venv
	@echo "📦 Installing dependencies..."
	@. environment/venv/bin/activate && pip install -r environment/requirements.txt
	@echo "✅ Setup complete! Activate with: source environment/venv/bin/activate"

install:
	@echo "📦 Installing dependencies..."
	@. environment/venv/bin/activate && pip install -r environment/requirements.txt
	@echo "✅ Dependencies installed!"

# Docker commands
docker-up:
	@echo "🐳 Starting Docker containers..."
	cd environment && docker compose up -d --build
	@echo "✅ Docker containers running!"
	@echo "   Access with: make docker-shell"

docker-down:
	@echo "🛑 Stopping Docker containers..."
	cd environment && docker compose down
	@echo "✅ Containers stopped!"

docker-logs:
	cd environment && docker compose logs -f

docker-shell:
	@echo "🐚 Opening shell in Docker container..."
	docker exec -it hotel_de_workbench bash

# Phase 1 commands
phase1-generate:
	@echo "🏨 Generating hotel booking data..."
	@cd projects/phase1-lifecycle && ../../environment/venv/bin/python scripts/generate_data.py
	@echo "✅ Data generated at: projects/phase1-lifecycle/data/raw_bookings.csv"

phase1-analyze:
	@echo "📊 Analyzing hotel bookings..."
	@cd projects/phase1-lifecycle && ../../environment/venv/bin/python scripts/analyze_data.py

phase1-full: phase1-generate phase1-analyze
	@echo "✅ Phase 1 pipeline complete!"

# Phase 1 Docker commands
phase1-generate-docker:
	@echo "🏨 Generating hotel booking data (Docker)..."
	docker exec -it hotel_de_workbench bash -c "cd projects/phase1-lifecycle && python scripts/generate_data.py"

phase1-analyze-docker:
	@echo "📊 Analyzing hotel bookings (Docker)..."
	docker exec -it hotel_de_workbench bash -c "cd projects/phase1-lifecycle && python scripts/analyze_data.py"

phase1-full-docker: phase1-generate-docker phase1-analyze-docker
	@echo "✅ Phase 1 pipeline complete (Docker)!"

# Cleanup commands
clean:
	@echo "🧹 Cleaning generated files..."
	find projects -name "*.csv" -type f -delete
	find projects -name "*.duckdb" -type f -delete
	find projects -name "*.db" -type f -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

clean-all: clean docker-down
	@echo "🧹 Removing virtual environment..."
	rm -rf environment/venv
	@echo "✅ Full cleanup complete!"

# Test commands
test:
	@echo "🧪 Running tests..."
	@echo "⚠️  Tests not yet implemented"
	@echo "   Add your tests in: projects/phase1-lifecycle/tests/"
