# Data Engineering Journey 🚀

My personal learning journey from **Frontend Developer** to **Data Engineer** with a focus on **Hotel Tech**.

## 📂 Project Structure

```
data-engineer-journey/
├── environment/          # Shared development environment (Docker, venv, dependencies)
├── projects/             # Phase-specific projects and code
├── docs/                 # Learning notes and documentation
└── plans/                # Learning roadmap and phase plans
```

## 🎯 Learning Phases

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Data Engineering Lifecycle & SQL | 🔄 In Progress |
| **Phase 2** | Infrastructure & Modern Data Stack | 📅 Planned |
| **Phase 3** | Orchestration & Distributed Systems | 📅 Planned |
| **Phase 4** | End-to-End Portfolio Project | 📅 Planned |

## 🛠 Tech Stack

- **Languages:** Python, SQL
- **Databases:** PostgreSQL, DuckDB
- **Processing:** Pandas, Polars, PySpark
- **Infrastructure:** Docker, dbt, Airflow
- **Cloud:** S3, Snowflake/BigQuery

## 🚀 Quick Start

### One-Time Setup
```bash
make setup
```

### Run Phase 1
```bash
make phase1-full
```

That's it! See [QUICKSTART.md](QUICKSTART.md) for detailed guide.

### All Available Commands
```bash
make help
```

#### Common Commands
- `make phase1-generate` - Generate hotel booking data
- `make phase1-analyze` - Run SQL analysis
- `make docker-up` - Start Docker containers
- `make clean` - Remove generated files

See [docs/COMMANDS.md](docs/COMMANDS.md) for complete reference.

## 📚 Documentation

### Core Learning Guides
- [📖 Data Engineering Lifecycle](docs/learning-notes/data-engineering-lifecycle.md) - 5 stages explained with hotel examples
- [🏨 Hotel Source Systems](docs/learning-notes/hotel-source-systems.md) - PMS, POS, CRS deep dive
- [📊 Hotel Metrics](docs/learning-notes/hotel-metrics.md) - ADR, RevPAR, Occupancy calculations
- [🦆 DuckDB Tips](docs/learning-notes/duckdb-tips.md) - SQL patterns and best practices

### Quick References
- [Commands Guide](docs/COMMANDS.md) - All Makefile commands explained
- [Learning Resources](docs/resources.md) - Free courses, datasets, books
- [Architecture Docs](docs/architecture/data-model.md) - Data modeling patterns

## 🎓 Skills Building

- ✅ Python for data processing
- ✅ Analytical SQL (Window Functions, CTEs)
- 🔄 Star Schema modeling for hotel data
- 📅 Data pipeline orchestration
- 📅 Distributed computing with Spark

---

**Started:** January 2026  
**Goal:** Become a proficient Data Engineer in the Hotel Tech industry
