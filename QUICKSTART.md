# Quick Start Guide 🚀

Get up and running in 2 minutes!

## TL;DR (Too Long; Didn't Read)

```bash
# Setup (only once)
make setup

# Run Phase 1
make phase1-full

# Done! 🎉
```

---

## Step-by-Step Guide

### 1️⃣ Clone & Setup (First Time Only)

```bash
cd data-engineer-journey
make setup
```

This creates a virtual environment and installs all dependencies.

### 2️⃣ Run Your First Data Pipeline

```bash
make phase1-full
```

This will:
1. Generate 500 hotel booking records
2. Analyze them with DuckDB SQL
3. Show ADR, revenue, and occupancy metrics

### 3️⃣ See the Results

Open the generated data:
```bash
cat projects/phase1-lifecycle/data/raw_bookings.csv | head
```

---

## What's Next?

### Learn the Commands
```bash
make help
```

### Explore the Data
```bash
# Generate new data
make phase1-generate

# Analyze existing data
make phase1-analyze
```

### Use Docker (Alternative)
```bash
make docker-up
make phase1-full-docker
```

### Clean Up
```bash
make clean        # Remove generated files
make clean-all    # Remove everything including venv
```

---

## Command Cheat Sheet

| Command | What It Does |
|---------|--------------|
| `make setup` | First-time environment setup |
| `make phase1-full` | Run complete Phase 1 pipeline |
| `make phase1-generate` | Generate sample hotel data |
| `make phase1-analyze` | Analyze data with SQL |
| `make docker-up` | Start Docker containers |
| `make docker-shell` | Open shell in container |
| `make clean` | Remove generated files |
| `make help` | Show all commands |

---

## Need Help?

- **Commands**: See [docs/COMMANDS.md](docs/COMMANDS.md)
- **Hotel Metrics**: See [docs/learning-notes/hotel-metrics.md](docs/learning-notes/hotel-metrics.md)
- **DuckDB SQL**: See [docs/learning-notes/duckdb-tips.md](docs/learning-notes/duckdb-tips.md)
- **Phase 1 Plan**: See [plans/Phase1_The_Pivot.md](plans/Phase1_The_Pivot.md)

---

## Troubleshooting

### "make: command not found"
Install Make:
```bash
brew install make  # macOS
```

### "No module named 'duckdb'"
Run setup again:
```bash
make setup
```

### "Permission denied"
Make scripts executable:
```bash
chmod +x scripts/*.sh
```

---

**Happy Learning! 🎓**
