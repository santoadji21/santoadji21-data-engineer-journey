# Command Reference 📖

Quick reference for all Makefile commands and scripts.

## 🎯 Most Used Commands

```bash
# Setup everything (first time only)
make setup

# Run Phase 1 complete pipeline
make phase1-full

# View all available commands
make help
```

## 📦 Environment Setup

### Initial Setup
```bash
make setup
```
Creates virtual environment and installs all dependencies.

### Install Dependencies Only
```bash
make install
```
Installs Python packages without recreating venv.

### Manual Setup
```bash
./scripts/setup.sh
```
Interactive setup script with helpful messages.

---

## 🐳 Docker Commands

### Start Containers
```bash
make docker-up
```
Builds and starts Docker containers in detached mode.

### Stop Containers
```bash
make docker-down
```
Stops and removes Docker containers.

### View Logs
```bash
make docker-logs
```
Streams Docker container logs (Ctrl+C to exit).

### Open Shell in Container
```bash
make docker-shell
```
Opens an interactive bash shell inside the running container.

---

## 🏨 Phase 1: Hotel Lifecycle

### Local Execution

#### Generate Sample Data
```bash
make phase1-generate
```
Creates `projects/phase1-lifecycle/data/raw_bookings.csv` with 500 bookings.

#### Analyze Data
```bash
make phase1-analyze
```
Runs DuckDB SQL queries to calculate ADR, revenue, and occupancy.

#### Complete Pipeline
```bash
make phase1-full
```
Runs generate → analyze in sequence.

### Docker Execution

```bash
make phase1-generate-docker  # Generate in container
make phase1-analyze-docker   # Analyze in container
make phase1-full-docker      # Full pipeline in container
```

### Bash Script (Alternative)

```bash
./scripts/run-phase1.sh           # Local execution
./scripts/run-phase1.sh --docker  # Docker execution
```

---

## 🧹 Cleanup Commands

### Clean Generated Files
```bash
make clean
```
Removes:
- CSV files
- DuckDB databases
- Python cache (`__pycache__`, `*.pyc`)

### Full Cleanup
```bash
make clean-all
```
Removes everything including:
- Virtual environment
- Docker containers
- All generated files

---

## 💡 Tips & Tricks

### Chain Commands
```bash
make setup && make phase1-full
```

### Run in Background
```bash
make docker-up && make phase1-full-docker &
```

### Quick Data Regeneration
```bash
make clean && make phase1-generate
```

### Check If Docker is Running
```bash
docker ps | grep hotel_de_workbench
```

---

## 🔧 Troubleshooting

### "Command not found: make"
Install GNU Make:
```bash
# macOS
brew install make

# Linux
sudo apt-get install make
```

### "Permission denied" for scripts
Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Python module not found
Reinstall dependencies:
```bash
make install
# Or
source environment/venv/bin/activate && pip install -r environment/requirements.txt
```

### Docker container not starting
Check logs:
```bash
make docker-logs
```

---

## 📚 Related Documentation

- [Hotel Metrics Guide](learning-notes/hotel-metrics.md) - Understanding ADR, RevPAR
- [DuckDB Tips](learning-notes/duckdb-tips.md) - SQL patterns and examples
- [Phase 1 README](../projects/phase1-lifecycle/README.md) - Phase-specific details
