"""
Seed script: generates realistic mock hotel data into DuckDB.

Creates the gold-layer tables that the FastAPI backend reads:
  - gold_revenue_by_hotel: daily revenue, ADR, RevPAR, occupancy, cancellation per hotel
  - gold_occupancy_rate: daily occupancy rate per hotel

Hotels:
  1. The Grand Budapest (legacy)  – High ADR, low cancellation, long stays
  2. Seaside Resort (modern)      – Seasonal spikes, family bookings
  3. City Budget Inn (budget)     – High volume, short stays, high cancellation
"""

import os
import random
from datetime import date, timedelta
from pathlib import Path

import duckdb

DUCKDB_PATH = os.environ.get(
    "DUCKDB_PATH",
    str(Path(__file__).resolve().parent.parent / "data" / "hotel_dashboard.duckdb"),
)

HOTELS = {
    "grand_budapest": {"total_rooms": 200, "base_adr": 280, "base_occ": 0.78, "cancel_rate": 0.08},
    "seaside_resort": {"total_rooms": 150, "base_adr": 190, "base_occ": 0.65, "cancel_rate": 0.15},
    "city_budget_inn": {"total_rooms": 100, "base_adr": 75, "base_occ": 0.88, "cancel_rate": 0.25},
}

SEED_DAYS = 90
random.seed(42)


def seasonal_factor(d: date, hotel_id: str) -> float:
    """Simulate seasonal variation."""
    day_of_year = d.timetuple().tm_yday
    base = 1.0

    if hotel_id == "seaside_resort":
        # Summer peak (June-Aug), winter low
        if 150 <= day_of_year <= 240:
            base = 1.3
        elif day_of_year <= 60 or day_of_year >= 330:
            base = 0.7

    if hotel_id == "grand_budapest":
        # Holiday peaks
        if 340 <= day_of_year or day_of_year <= 10:
            base = 1.2

    # Weekend bump for all hotels
    if d.weekday() >= 5:
        base *= 1.1

    return base


def generate_data() -> list[dict]:
    """Generate daily metrics for each hotel."""
    rows = []
    end_date = date.today()
    start_date = end_date - timedelta(days=SEED_DAYS)

    for hotel_id, cfg in HOTELS.items():
        current = start_date
        while current <= end_date:
            factor = seasonal_factor(current, hotel_id)
            noise = random.uniform(0.9, 1.1)

            occupancy_rate = min(cfg["base_occ"] * factor * noise, 0.99)
            rooms_sold = int(cfg["total_rooms"] * occupancy_rate)
            adr = round(cfg["base_adr"] * factor * random.uniform(0.92, 1.08), 2)
            revenue = round(rooms_sold * adr, 2)
            revpar = round(revenue / cfg["total_rooms"], 2)

            cancel_noise = random.uniform(0.7, 1.3)
            cancellation_rate = round(min(cfg["cancel_rate"] * cancel_noise, 0.5), 4)

            total_bookings = rooms_sold + int(rooms_sold * cancellation_rate)

            rows.append(
                {
                    "date": current,
                    "hotel_id": hotel_id,
                    "revenue": revenue,
                    "adr": adr,
                    "revpar": revpar,
                    "occupancy_rate": round(occupancy_rate, 4),
                    "cancellation_rate": cancellation_rate,
                    "rooms_sold": rooms_sold,
                    "total_rooms": cfg["total_rooms"],
                    "total_bookings": total_bookings,
                }
            )
            current += timedelta(days=1)

    return rows


def seed() -> None:
    """Write generated data into DuckDB."""
    data_dir = Path(DUCKDB_PATH).parent
    data_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing DB so we start fresh
    db_path = Path(DUCKDB_PATH)
    if db_path.exists():
        db_path.unlink()
    wal_path = db_path.with_suffix(".duckdb.wal")
    if wal_path.exists():
        wal_path.unlink()

    print(f"Seeding DuckDB at: {DUCKDB_PATH}")
    rows = generate_data()
    print(f"Generated {len(rows)} rows across {len(HOTELS)} hotels ({SEED_DAYS} days)")

    con = duckdb.connect(str(DUCKDB_PATH))

    con.execute("""
        CREATE TABLE gold_revenue_by_hotel (
            date         DATE NOT NULL,
            hotel_id     VARCHAR NOT NULL,
            revenue      DOUBLE NOT NULL,
            adr          DOUBLE NOT NULL,
            revpar       DOUBLE NOT NULL,
            occupancy_rate   DOUBLE NOT NULL,
            cancellation_rate DOUBLE NOT NULL,
            rooms_sold   INTEGER NOT NULL,
            total_rooms  INTEGER NOT NULL,
            total_bookings INTEGER NOT NULL
        )
    """)

    con.execute("""
        CREATE TABLE gold_occupancy_rate (
            date         DATE NOT NULL,
            hotel_id     VARCHAR NOT NULL,
            occupancy_rate DOUBLE NOT NULL,
            rooms_sold   INTEGER NOT NULL,
            total_rooms  INTEGER NOT NULL
        )
    """)

    con.executemany(
        """
        INSERT INTO gold_revenue_by_hotel
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r["date"],
                r["hotel_id"],
                r["revenue"],
                r["adr"],
                r["revpar"],
                r["occupancy_rate"],
                r["cancellation_rate"],
                r["rooms_sold"],
                r["total_rooms"],
                r["total_bookings"],
            )
            for r in rows
        ],
    )

    con.executemany(
        """
        INSERT INTO gold_occupancy_rate
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                r["date"],
                r["hotel_id"],
                r["occupancy_rate"],
                r["rooms_sold"],
                r["total_rooms"],
            )
            for r in rows
        ],
    )

    count = con.execute("SELECT COUNT(*) FROM gold_revenue_by_hotel").fetchone()
    print(f"Inserted {count[0]} rows into gold_revenue_by_hotel")

    count = con.execute("SELECT COUNT(*) FROM gold_occupancy_rate").fetchone()
    print(f"Inserted {count[0]} rows into gold_occupancy_rate")

    con.close()
    print("Seed complete.")


if __name__ == "__main__":
    seed()
