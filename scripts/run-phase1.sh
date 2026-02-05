#!/bin/bash

# Quick script to run Phase 1 complete pipeline
# Usage: ./scripts/run-phase1.sh [--docker]

set -e

if [ "$1" == "--docker" ]; then
    echo "🐳 Running Phase 1 in Docker..."
    echo ""
    
    # Check if container is running
    if ! docker ps | grep -q hotel_de_workbench; then
        echo "⚠️  Docker container not running. Starting..."
        cd environment && docker compose up -d
        cd ..
        sleep 2
    fi
    
    echo "🏨 Step 1: Generating hotel booking data..."
    docker exec hotel_de_workbench bash -c "cd projects/phase1-lifecycle && python scripts/generate_data.py"
    echo ""
    
    echo "📊 Step 2: Analyzing bookings with DuckDB..."
    docker exec hotel_de_workbench bash -c "cd projects/phase1-lifecycle && python scripts/analyze_data.py"
    
else
    echo "🏨 Running Phase 1 locally..."
    echo ""
    
    # Check if venv exists
    if [ ! -d "environment/venv" ]; then
        echo "❌ Virtual environment not found. Run: make setup"
        exit 1
    fi
    
    # Activate venv
    source environment/venv/bin/activate
    
    echo "🏨 Step 1: Generating hotel booking data..."
    cd projects/phase1-lifecycle
    python scripts/generate_data.py
    echo ""
    
    echo "📊 Step 2: Analyzing bookings with DuckDB..."
    python scripts/analyze_data.py
    cd ../..
fi

echo ""
echo "✅ Phase 1 pipeline complete! 🎉"
echo ""
echo "📂 Data location: projects/phase1-lifecycle/data/"
echo "📖 Learn more:    docs/learning-notes/hotel-metrics.md"
