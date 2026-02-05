#!/bin/bash

# Setup script for Data Engineering Journey
# This script sets up the entire development environment

set -e  # Exit on error

echo "🚀 Setting up Data Engineering Journey..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
cd environment
python3 -m venv venv
echo "✅ Virtual environment created!"
echo ""

# Activate and install dependencies
echo "📚 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed!"
echo ""

# Create data directories
echo "📁 Creating project directories..."
cd ..
mkdir -p projects/phase1-lifecycle/data
mkdir -p projects/phase1-lifecycle/notebooks
mkdir -p projects/phase2-infrastructure
mkdir -p projects/phase3-orchestration
mkdir -p projects/phase4-portfolio
echo "✅ Directories created!"
echo ""

# Check Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
    echo ""
    echo "🐳 You can now run: make docker-up"
else
    echo "⚠️  Docker not found. Install Docker to use containerized environment."
fi

echo ""
echo "✅ Setup complete! 🎉"
echo ""
echo "Quick Start:"
echo "  1. Activate environment: source environment/venv/bin/activate"
echo "  2. Generate data:        make phase1-generate"
echo "  3. Analyze data:         make phase1-analyze"
echo ""
echo "Or use Docker:"
echo "  1. Start containers:     make docker-up"
echo "  2. Run in Docker:        make phase1-full-docker"
echo ""
echo "See all commands:        make help"
