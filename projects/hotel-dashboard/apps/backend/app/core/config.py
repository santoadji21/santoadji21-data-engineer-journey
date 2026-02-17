import os
from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DUCKDB_PATH = os.environ.get("DUCKDB_PATH", str(DATA_DIR / "hotel_dashboard.duckdb"))


class HotelConfig(BaseModel):
    hotel_id: str
    name: str
    pms_type: str
    total_rooms: int


HOTELS: list[HotelConfig] = [
    HotelConfig(
        hotel_id="grand_budapest",
        name="The Grand Budapest",
        pms_type="legacy",
        total_rooms=200,
    ),
    HotelConfig(
        hotel_id="seaside_resort",
        name="Seaside Resort",
        pms_type="modern",
        total_rooms=150,
    ),
    HotelConfig(
        hotel_id="city_budget_inn",
        name="City Budget Inn",
        pms_type="budget",
        total_rooms=100,
    ),
]
