# Documentation 📚

Welcome to your data engineering learning hub! This documentation grows with you as you progress through the phases.

## 🎯 Quick Navigation

### Getting Started
- [QUICKSTART.md](../QUICKSTART.md) - Get running in 2 minutes
- [COMMANDS.md](COMMANDS.md) - Complete command reference

### Core Concepts
- [Data Engineering Lifecycle](learning-notes/data-engineering-lifecycle.md) ⭐ **START HERE**
- [Hotel Source Systems](learning-notes/hotel-source-systems.md) - PMS, POS, CRS deep dive
- [Hotel Metrics Explained](learning-notes/hotel-metrics.md) - ADR, RevPAR, Occupancy

### Technical Guides
- [DuckDB Tips & Tricks](learning-notes/duckdb-tips.md) - SQL patterns and examples
- [Data Model Architecture](architecture/data-model.md) - Star schema design

### Resources
- [Learning Resources](resources.md) - Free courses, datasets, books

---

## 📖 Learning Path

### Phase 1: The Pivot (You Are Here)
**Focus:** Understanding the fundamentals

**Must Read:**
1. [Data Engineering Lifecycle](learning-notes/data-engineering-lifecycle.md)
   - 5 stages: Generation → Ingestion → Storage → Transformation → Serving
   - Batch vs. Streaming
   - Data Lakes vs. Data Warehouses

2. [Hotel Source Systems](learning-notes/hotel-source-systems.md)
   - Where hotel data comes from (PMS, POS, CRS)
   - How to extract data (APIs, databases, files)
   - Common challenges and solutions

3. [Hotel Metrics Explained](learning-notes/hotel-metrics.md)
   - ADR (Average Daily Rate)
   - RevPAR (Revenue Per Available Room)
   - Occupancy calculations
   - SQL examples for each metric

4. [DuckDB Tips](learning-notes/duckdb-tips.md)
   - Why DuckDB for analytics
   - Window functions, CTEs
   - Export patterns

**Hands-On:**
- Run `make phase1-full` to generate and analyze hotel data
- Practice SQL queries in `projects/phase1-lifecycle/`

### Phase 2: Infrastructure (Coming Soon)
**Focus:** dbt, Docker, Modern Data Stack

**Topics:**
- Medallion Architecture (Bronze/Silver/Gold)
- dbt models and testing
- Infrastructure as Code (Terraform)

### Phase 3: Orchestration (Coming Soon)
**Focus:** Airflow, Spark, Streaming

**Topics:**
- DAG design patterns
- Distributed processing
- Real-time pipelines

### Phase 4: Portfolio (Coming Soon)
**Focus:** End-to-end production project

**Topics:**
- Complete hotel analytics platform
- Production best practices
- Interview preparation

---

## 📝 Documentation Structure

```
docs/
├── README.md                           # This file
├── COMMANDS.md                         # Command reference
├── resources.md                        # Learning resources
├── learning-notes/
│   ├── data-engineering-lifecycle.md  # ⭐ 5 stages explained
│   ├── hotel-source-systems.md        # ⭐ PMS, POS, CRS deep dive
│   ├── hotel-metrics.md               # ADR, RevPAR, Occupancy
│   └── duckdb-tips.md                 # SQL tips and tricks
└── architecture/
    └── data-model.md                  # Star schema design
```

---

## 🎓 How to Use This Documentation

### 1. **Read Before Coding**
Start with the lifecycle guide to understand the "why" before the "how".

### 2. **Reference During Projects**
Use the technical guides when implementing Phase 1 exercises.

### 3. **Take Notes**
Add your own markdown files in `learning-notes/` as you learn:
```bash
# Create your own notes
touch docs/learning-notes/my-sql-learnings.md
```

### 4. **Update as You Go**
This is YOUR documentation. Add examples, clarifications, and lessons learned.

---

## 💡 Study Tips

### For Concepts (Lifecycle, Systems)
1. Read the full doc
2. Summarize in your own words
3. Draw diagrams on paper

### For Technical Guides (DuckDB, Metrics)
1. Read the examples
2. Run them in your Phase 1 project
3. Modify and experiment

### For SQL
1. Copy the query
2. Change the logic (e.g., different metric)
3. Explain what each line does

---

## 🔗 External Resources

See [resources.md](resources.md) for:
- Data Engineering Zoomcamp (free course)
- Hotel datasets for practice
- SQL tutorials and books
- YouTube channels

---

## 📮 Keep Learning

As you progress:
- ✅ Check off items in `/plans/Phase1_The_Pivot.md`
- 📝 Document your learnings in `learning-notes/`
- 🚀 Build projects in `/projects/`
- 💬 Share what you learn (blog, LinkedIn)

---

**Happy Learning! 🎉**

*Last Updated: January 2026 - Phase 1*
