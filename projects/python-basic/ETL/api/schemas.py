"""
Pydantic schemas for request/response validation.

Pydantic models define the SHAPE of data flowing through the API.
FastAPI uses them to:
  - Auto-validate incoming JSON bodies
  - Auto-generate OpenAPI/Swagger docs
  - Serialize responses to JSON
"""

from pydantic import BaseModel, Field
from datetime import date


# ============================================================
# Request Schemas (what the client SENDS)
# ============================================================

class BookingCreate(BaseModel):
    """
    Schema for creating a new booking via POST.

    BaseModel is the base class for all Pydantic models.
    Field() adds validation constraints and metadata.
    """

    hotel: str = Field(
        ...,                          # ... = required (no default)
        description="Hotel type",
        examples=["City Hotel", "Resort Hotel"],
    )
    guest_name: str = Field(
        ...,
        min_length=1,                 # min_length validates string length
        max_length=100,
        description="Guest full name",
    )
    country: str = Field(
        default="UNKNOWN",            # default value if not provided
        min_length=2,
        max_length=5,
        description="ISO country code (e.g. PRT, GBR)",
    )
    adr: float = Field(
        ...,
        gt=0,                         # gt = greater than (must be positive)
        le=10000,                     # le = less than or equal
        description="Average Daily Rate in USD",
    )
    total_nights: int = Field(
        ...,
        ge=1,                         # ge = greater than or equal
        le=365,
        description="Total nights of stay",
    )
    arrival_date: date = Field(
        ...,
        description="Arrival date (YYYY-MM-DD)",
    )

    # model_config controls Pydantic behavior
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "hotel": "City Hotel",
                    "guest_name": "Alya Rahman",
                    "country": "IDN",
                    "adr": 120.50,
                    "total_nights": 3,
                    "arrival_date": "2026-03-15",
                }
            ]
        }
    }


# ============================================================
# Response Schemas (what the API RETURNS)
# ============================================================

class BookingResponse(BaseModel):
    """Schema for a single booking in API responses."""

    id: int
    hotel: str
    guest_name: str
    country: str
    adr: float
    total_nights: int
    total_revenue: float              # computed: adr * total_nights
    arrival_date: date


class BookingSummary(BaseModel):
    """Schema for aggregated booking statistics."""

    total_bookings: int
    total_revenue: float
    avg_adr: float
    top_countries: list[dict]         # list of {"country": str, "count": int}


class PipelineStatus(BaseModel):
    """Schema for pipeline execution status."""

    status: str = Field(..., description="Pipeline status: running, success, failed")
    message: str
    rows_processed: int = 0
    output_file: str | None = None    # str | None = optional field (can be null)
